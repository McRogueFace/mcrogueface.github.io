#!/usr/bin/env python3
"""build_library.py -- generate the McRogueFace docs-site "Library" gallery.

Produces:
  library/index.md            Gallery of playground snippets, engine demo
                              screens, and (placeholder) games.
  library/_thumbnails_todo.md Follow-up checklist of demo-screen thumbnails
                              that still need to be copied into the site.

Everything is pure python3 stdlib. Source links are pinned:
  * Snippets live in THIS (site) repo   -> pinned to the site HEAD sha.
  * Demo screens / games live in the    -> pinned to --ref (default: engine
    engine repo                            HEAD sha, or tag 0.2.8 if it has
                                           been pushed to the github remote).

Usage:
    python3 tools/build_library.py [--ref <sha-or-tag>]

The --ref argument overrides the engine-repo pin used for demo-screen and
game source links. It has no effect on snippet links (always site repo).
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).parent))
from lzstring import compress_to_encoded_uri_component  # noqa: E402

# --- Fixed locations ---------------------------------------------------------
SITE_ROOT = Path("/home/john/Development/mcrogueface.github.io")
ENGINE_ROOT = Path("/home/john/Development/McRogueFace")

# The snippets live in the ENGINE repo (tests/snippets/), not here. They are executed by
# McRogueFace's test suite, so breaking the API breaks the build -- and the `status=ok`
# in each snippet's `# mcrf:` header is stamped by an actual run rather than typed by
# hand. The site pulls them from there; it does not keep a copy to rot in parallel.
SNIPPETS_DIR = ENGINE_ROOT / "tests" / "snippets"
LIBRARY_DIR = SITE_ROOT / "library"
DEMO_SCREENS_DIR = ENGINE_ROOT / "tests" / "demo" / "screens"
DEMO_SHOTS_DIR = ENGINE_ROOT / "tests" / "demo" / "screenshots"
GAMES_DIR = ENGINE_ROOT / "games"

# Snippet preview screenshots: a generated, gitignored artifact in the ENGINE repo,
# produced by `make snippet-shots` (#381). They are copied INTO this site repo, where
# they are served and committed -- the engine repo never carries them. SRC is where the
# engine writes them; DST is the served, committed location here.
SNIPPET_SHOTS_SRC = ENGINE_ROOT / "snippet-shots"
SNIPPET_SHOTS_DST = SITE_ROOT / "assets" / "images" / "snippet-shots"
# Web path (Jekyll baseurl-relative) used in <img src>.
SNIPPET_SHOTS_WEB = "/assets/images/snippet-shots"

# The deployed playground reads shared code from the URL fragment
# (see src/shell.html: parseUrlFragment):
#   #src=<lz-string>   inline, self-contained, no git ref -> can't rot
#   #url=<raw file>    playground fetches raw.githubusercontent.com at a pinned
#                      commit (CORS-open); used when the inline form is too long
# Short snippets go inline; long ones (compressed > INLINE_URL_LIMIT) use the
# raw-file loader pinned to the snippet commit sha.
PLAYGROUND_WEB = "/playground/"
INLINE_URL_LIMIT = 1024  # compressed #src= chars above which we switch to #url=


def playground_url(info: dict, engine_slug, snippet_ref) -> str:
    """Baseurl-relative Open-in-Playground link for one snippet.

    Inline (#src=) when the compressed source is short; otherwise a raw-file
    (#url=) link pinned to `snippet_ref`. Falls back to inline if the engine
    github slug is unknown -- a long URL still works, a broken raw link doesn't.
    """
    compressed = compress_to_encoded_uri_component(info["source"])
    if len(compressed) <= INLINE_URL_LIMIT or not engine_slug:
        frag = f"#src={compressed}"
    else:
        rel = f"tests/snippets/{info['stem']}.py"
        raw = raw_url(engine_slug, snippet_ref, rel)
        frag = f"#url={quote(raw, safe='')}"
    return f"{{{{ site.baseurl }}}}{PLAYGROUND_WEB}{frag}"

# Fallback pins used only when git is unavailable / detached in a way that
# rev-parse cannot resolve. These are the known-good HEAD shas at authoring
# time (site HEAD b3819c0, engine HEAD b6720f6).
FALLBACK_SITE_REF = "b3819c0"
FALLBACK_ENGINE_REF = "b6720f6"

RELEASE_TAG = "0.2.8"

# Demo-screen helper files that are infrastructure, not showcase screens.
DEMO_SKIP = {"__init__.py", "base.py"}


# --- git helpers -------------------------------------------------------------
def git(repo: Path, *args) -> str | None:
    """Run a git command in `repo`, returning stripped stdout or None on error."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def head_sha(repo: Path, fallback: str) -> str:
    sha = git(repo, "rev-parse", "--short=7", "HEAD")
    return sha if sha else fallback


def remotes(repo: Path) -> dict[str, str]:
    """Map remote-name -> fetch URL."""
    out = git(repo, "remote", "-v")
    result: dict[str, str] = {}
    if not out:
        return result
    for line in out.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[2] == "(fetch)":
            result[parts[0]] = parts[1]
    return result


def github_slug(repo: Path, preferred_order) -> str | None:
    """Return 'owner/repo' for the first github.com remote, honoring priority."""
    rem = remotes(repo)
    # Try named remotes in priority order first, then any remaining github one.
    names = [n for n in preferred_order if n in rem] + \
            [n for n in rem if n not in preferred_order]
    for name in names:
        url = rem[name]
        if "github.com" not in url:
            continue
        # git@github.com:owner/repo.git  OR  https://github.com/owner/repo.git
        m = re.search(r"github\.com[:/]([^/]+/[^/]+?)(?:\.git)?/?$", url)
        if m:
            return m.group(1)
    return None


def tag_on_remote(repo: Path, remote: str, tag: str) -> bool:
    out = git(repo, "ls-remote", "--tags", remote, tag)
    return bool(out)


def full_head_sha(repo: Path) -> str | None:
    return git(repo, "rev-parse", "HEAD")


def snippets_dirty(repo: Path) -> bool:
    """True if the snippet dir has uncommitted changes -- then no commit sha
    faithfully represents what we are rendering, so a raw-file pin would serve
    different bytes than the previews. Caller must fail rather than pin."""
    out = git(repo, "status", "--porcelain", "tests/snippets/")
    return bool(out)


def sha_on_remote(repo: Path, remote: str, sha: str) -> bool:
    """Is `sha` reachable from a branch on `remote` (i.e. actually pushed)?"""
    out = git(repo, "branch", "-r", "--contains", sha)
    if not out:
        return False
    return any(ln.strip().startswith(f"{remote}/") for ln in out.splitlines())


def raw_url(slug: str, ref: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{slug}/{ref}/{path}"


def blob_url(slug: str, ref: str, path: str) -> str:
    return f"https://github.com/{slug}/blob/{ref}/{path}"


# --- snippet parsing ---------------------------------------------------------
META_RE = re.compile(r"^#\s*mcrf:\s*(.*)$")


def title_from_stem(stem: str) -> str:
    """`031_animation_basic` -> 'Animation Basic'."""
    body = re.sub(r"^\d+_", "", stem)
    return body.replace("_", " ").title()


def category_from_stem(stem: str) -> str:
    """First token after the numeric prefix, e.g. 'animation', 'grid'."""
    body = re.sub(r"^\d+_", "", stem)
    tok = body.split("_", 1)[0]
    return tok


def parse_snippet(path: Path) -> dict:
    """Extract title, description, and `# mcrf:` metadata from a snippet."""
    info = {
        "stem": path.stem,
        "number": path.stem.split("_", 1)[0],
        "title": title_from_stem(path.stem),
        "desc": "",
        "objects": [],
        "status": "",
        "verified": "",
        "source": "",
    }
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return info
    info["source"] = text
    lines = text.splitlines()

    for line in lines[:8]:
        stripped = line.strip()
        m = META_RE.match(stripped)
        if m:
            payload = m.group(1)
            objs = re.search(r"objects=\[([^\]]*)\]", payload)
            if objs:
                info["objects"] = [
                    o.strip() for o in objs.group(1).split(",") if o.strip()
                ]
            st = re.search(r"status=(\S+)", payload)
            if st:
                info["status"] = st.group(1)
            ver = re.search(r"verified=(\S+)", payload)
            if ver:
                info["verified"] = ver.group(1)
            continue
        # First non-meta, non-shebang comment line becomes the description.
        if not info["desc"] and stripped.startswith("#") and \
                not stripped.startswith("#!"):
            info["desc"] = stripped.lstrip("#").strip()
    return info


# --- snippet preview screenshots ---------------------------------------------
def sync_snippet_shots() -> set[str]:
    """Copy the engine's snippet screenshots into this repo; return the stems copied.

    The PNGs are a generated, gitignored artifact in the engine (#381); this repo is
    where they are served and committed. Fails loudly if they are absent rather than
    quietly shipping a gallery with no previews -- run `make snippet-shots` in the
    engine first (release-docs chains it)."""
    shots = (sorted(SNIPPET_SHOTS_SRC.glob("[0-9]*.png"))
             if SNIPPET_SHOTS_SRC.is_dir() else [])
    if not shots:
        sys.exit(
            f"build_library: no snippet screenshots in {SNIPPET_SHOTS_SRC}.\n"
            "  Run `make snippet-shots` in the engine repo first "
            "(release-docs chains it).")
    SNIPPET_SHOTS_DST.mkdir(parents=True, exist_ok=True)
    # Refresh: drop stale images so a removed or renamed snippet leaves no orphan.
    for old in SNIPPET_SHOTS_DST.glob("*.png"):
        old.unlink()
    stems = set()
    for src in shots:
        shutil.copy2(src, SNIPPET_SHOTS_DST / src.name)
        stems.add(src.stem)
    return stems


# --- section builders --------------------------------------------------------
def build_snippets_section(shots, engine_slug, snippet_ref) -> tuple[str, dict]:
    snippets = sorted(SNIPPETS_DIR.glob("[0-9]*.py"))
    parsed = [parse_snippet(p) for p in snippets]

    out = []
    out.append("## Playground Snippets\n")
    out.append(
        f"{len(parsed)} focused, copy-paste examples covering the whole "
        "`mcrfpy` API. Each snippet fills the 1024x768 playground canvas.\n")
    out.append(
        "> **Open in Playground** opens the exact code shown here in the "
        "[playground]({{ site.baseurl }}/playground/) &mdash; press Run "
        "(Ctrl+Enter). Short snippets travel inline in the URL "
        "(LZString-compressed `#src=`); longer ones load the raw file from the "
        "pinned commit (`#url=`). No copy-paste either way.\n")

    counts = {"inline": 0, "raw": 0}

    # Group by leading category token, preserving first-seen order.
    groups: dict[str, list] = {}
    for info in parsed:
        groups.setdefault(category_from_stem(info["stem"]), []).append(info)

    for cat, items in groups.items():
        out.append(f"\n### {cat.replace('_', ' ').title()}\n")
        out.append("| Snippet | Preview | Source |")
        out.append("|---------|---------|--------|")
        for info in items:
            title = info["title"]
            if info["desc"]:
                title = f"**{title}**<br><span style=\"color:#888\">" \
                        f"{info['desc']}</span>"
            if info["stem"] in shots:
                src = f"{{{{ site.baseurl }}}}{SNIPPET_SHOTS_WEB}/{info['stem']}.png"
                preview = (f'<img src="{src}" alt="{info["title"]} preview" '
                           f'loading="lazy" width="220">')
            else:
                preview = "&mdash;"
            url = playground_url(info, engine_slug, snippet_ref)
            counts["raw" if "#url=" in url else "inline"] += 1
            link = f"[&#9654; Open in Playground]({url})"
            out.append(f"| {title} | {preview} | {link} |")
        out.append("")

    return "\n".join(out), counts


def build_demos_section(engine_slug, engine_ref):
    screens = sorted(
        p for p in DEMO_SCREENS_DIR.glob("*.py") if p.name not in DEMO_SKIP
    )
    rows = []
    thumb_available = 0
    thumb_missing = 0
    todo_missing = []
    for p in screens:
        thumb = DEMO_SHOTS_DIR / f"{p.stem}.png"
        if thumb.exists():
            state = "&#9989; available"
            thumb_available += 1
        else:
            state = "&#10060; missing"
            thumb_missing += 1
            todo_missing.append(p.stem)
        if engine_slug:
            rel = f"tests/demo/screens/{p.name}"
            link = f"[view]({blob_url(engine_slug, engine_ref, rel)}) &middot; " \
                   f"[raw]({raw_url(engine_slug, engine_ref, rel)})"
        else:
            link = "&mdash;"
        rows.append((p.stem, state, link))

    out = []
    out.append("## Engine Demo Screens\n")
    out.append(
        f"{len(screens)} interactive demo screens from the engine test "
        "harness (`tests/demo/screens/`). Run them with "
        "`./mcrogueface ../tests/demo/demo_main.py`.\n")
    if engine_slug is None:
        out.append("_(Could not resolve a github.com remote for the engine "
                   "repo; source links omitted.)_\n")
    out.append("| Screen | Thumbnail | Source |")
    out.append("|--------|-----------|--------|")
    for stem, state, link in rows:
        out.append(f"| `{stem}` | {state} | {link} |")
    out.append("")

    stats = {
        "screens": len(screens),
        "available": thumb_available,
        "missing": thumb_missing,
        "todo_missing": todo_missing,
    }
    return "\n".join(out), stats


def build_games_section(engine_slug, engine_ref):
    games = sorted(p for p in GAMES_DIR.iterdir() if p.is_dir()) \
        if GAMES_DIR.exists() else []
    out = []
    out.append("## Games\n")
    out.append(
        "Full games built on McRogueFace. Web/desktop packaging is **pending** "
        "&mdash; these are listed from the engine repo's `games/` directory "
        "and are not yet downloadable builds.\n")
    if not games:
        out.append("_(No game directories found.)_\n")
    else:
        out.append("| Game | Source | Status |")
        out.append("|------|--------|--------|")
        for g in games:
            if engine_slug:
                rel = f"games/{g.name}"
                link = f"[browse]({blob_url(engine_slug, engine_ref, rel)})"
            else:
                link = "&mdash;"
            out.append(f"| `{g.name}` | {link} | packaging pending |")
        out.append("")
    return "\n".join(out), [g.name for g in games]


def build_thumbnails_todo(stats):
    orphans = []
    if DEMO_SHOTS_DIR.exists():
        screen_stems = {
            p.stem for p in DEMO_SCREENS_DIR.glob("*.py")
            if p.name not in DEMO_SKIP
        }
        for shot in sorted(DEMO_SHOTS_DIR.glob("*.png")):
            if shot.stem not in screen_stems:
                orphans.append(shot.name)

    out = []
    out.append("# Thumbnails TODO\n")
    out.append(
        "Follow-up checklist for the Library gallery. Copying demo screenshots "
        "into the site is a separate task (not owned by the library "
        "generator). The generator only reports which thumbnails are "
        "present.\n")
    out.append(f"- Demo screens total: **{stats['screens']}**")
    out.append(f"- Thumbnails available (`<name>.png` present): "
               f"**{stats['available']}**")
    out.append(f"- Thumbnails missing: **{stats['missing']}**\n")

    out.append("## Demo screens missing a `<name>.png` thumbnail\n")
    if stats["todo_missing"]:
        for stem in stats["todo_missing"]:
            out.append(f"- [ ] `tests/demo/screenshots/{stem}.png` "
                       f"(for screen `{stem}`)")
    else:
        out.append("_None &mdash; every screen has a matching thumbnail._")
    out.append("")

    out.append("## Existing screenshots with no matching screen name\n")
    out.append(
        "These files already exist in `tests/demo/screenshots/` but do not "
        "match a screen stem, so they are not auto-detected as thumbnails. "
        "A human should decide which screen each belongs to (or rename).\n")
    if orphans:
        for name in orphans:
            out.append(f"- `{name}`")
    else:
        out.append("_None._")
    out.append("")
    return "\n".join(out)


# --- main --------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", default=None,
                    help="Engine-repo ref for demo/game source links "
                         "(default: tag 0.2.8 if pushed, else engine HEAD sha).")
    ap.add_argument("--snippet-ref", default=None,
                    help="Engine commit/tag that long snippets' raw-file "
                         "(#url=) playground links pin to (default: engine HEAD "
                         "sha, which must be pushed to github to resolve).")
    args = ap.parse_args()

    site_ref = head_sha(SITE_ROOT, FALLBACK_SITE_REF)
    site_slug = github_slug(SITE_ROOT, preferred_order=["origin", "goblin"])
    engine_slug = github_slug(ENGINE_ROOT, preferred_order=["github", "goblin"])

    # Resolve engine ref + report which pin was chosen.
    ref_note = ""
    if args.ref:
        engine_ref = args.ref
        ref_note = f"explicit --ref {engine_ref}"
    else:
        # Determine which remote name is the github.com one for tag checks.
        gh_remote = None
        for name, url in remotes(ENGINE_ROOT).items():
            if "github.com" in url:
                gh_remote = name
                break
        if gh_remote and tag_on_remote(ENGINE_ROOT, gh_remote, RELEASE_TAG):
            engine_ref = RELEASE_TAG
            ref_note = f"tag {RELEASE_TAG} (pushed to {gh_remote})"
        else:
            engine_ref = head_sha(ENGINE_ROOT, FALLBACK_ENGINE_REF)
            ref_note = (f"engine HEAD sha {engine_ref} "
                        f"(tag {RELEASE_TAG} not on remote)")

    # Resolve the commit that raw-file (#url=) snippet links pin to. It must
    # faithfully represent the snippet bytes we are rendering, so refuse to pin
    # if the snippet dir is dirty (Fail Early: no silently-wrong links).
    gh_remote = None
    for name, url in remotes(ENGINE_ROOT).items():
        if "github.com" in url:
            gh_remote = name
            break
    if args.snippet_ref:
        snippet_ref = args.snippet_ref
        snippet_ref_note = f"explicit --snippet-ref {snippet_ref}"
    else:
        if snippets_dirty(ENGINE_ROOT):
            sys.exit(
                "build_library: tests/snippets/ has uncommitted changes; no "
                "commit represents these bytes. Commit them, then rebuild (or "
                "pass --snippet-ref <sha/tag>). Raw-file playground links must "
                "pin to a faithful ref.")
        snippet_ref = full_head_sha(ENGINE_ROOT) or FALLBACK_ENGINE_REF
        snippet_ref_note = f"engine HEAD {snippet_ref[:7]}"
        if gh_remote and not sha_on_remote(ENGINE_ROOT, gh_remote, snippet_ref):
            snippet_ref_note += (
                f" -- WARNING: not yet on '{gh_remote}'; raw-file (#url=) links "
                f"404 until this commit is pushed")

    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)

    shots = sync_snippet_shots()
    snippets_md, snippet_link_counts = build_snippets_section(
        shots, engine_slug, snippet_ref)
    demos_md, demo_stats = build_demos_section(engine_slug, engine_ref)
    games_md, games = build_games_section(engine_slug, engine_ref)

    page = []
    page.append("---")
    page.append("layout: default")
    page.append("title: Library")
    page.append("---")
    page.append("")
    page.append("# Library\n")
    page.append(
        "A gallery of runnable examples for McRogueFace: bite-sized "
        "**playground snippets**, full **engine demo screens**, and "
        "**games**. Snippet links open the code straight in the playground; "
        "demo/game source links are pinned to a specific commit.\n")
    page.append(
        "<sub>Short snippets carry their source inline in the link; longer "
        f"ones load the raw file pinned to engine `{snippet_ref[:7]}`"
        + (f" ([{engine_slug}](https://github.com/{engine_slug}))" if engine_slug else "")
        + f". Demos/games pinned to engine `{engine_ref}`. "
        + "Generated by `tools/build_library.py`.</sub>\n")
    page.append(snippets_md)
    page.append(demos_md)
    page.append(games_md)

    index_path = LIBRARY_DIR / "index.md"
    index_path.write_text("\n".join(page), encoding="utf-8")

    todo_path = LIBRARY_DIR / "_thumbnails_todo.md"
    todo_path.write_text(build_thumbnails_todo(demo_stats), encoding="utf-8")

    # Report to stdout (consumed by the caller).
    print("build_library.py complete")
    print(f"  ref pinning: {ref_note}")
    print(f"  site ref:    {site_ref}  slug: {site_slug}")
    print(f"  engine ref:  {engine_ref}  slug: {engine_slug}")
    print(f"  snippet ref: {snippet_ref_note}")
    print(f"  snippets:    {len(sorted(SNIPPETS_DIR.glob('[0-9]*.py')))} "
          f"({len(shots)} with previews -> {SNIPPET_SHOTS_DST})")
    print(f"  play links:  {snippet_link_counts['inline']} inline (#src=) / "
          f"{snippet_link_counts['raw']} raw-file (#url=)")
    print(f"  demo screens: {demo_stats['screens']} "
          f"(thumbnails {demo_stats['available']} available / "
          f"{demo_stats['missing']} missing)")
    print(f"  games:       {len(games)} -> {games}")
    print(f"  wrote: {index_path}")
    print(f"  wrote: {todo_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
