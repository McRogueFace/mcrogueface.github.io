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
    }
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return info

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


def status_badge(status: str) -> str:
    if not status:
        return "&mdash;"
    icons = {"ok": "&#9989; ok", "broken": "&#10060; broken",
             "wip": "&#128679; wip", "partial": "&#9888; partial"}
    return icons.get(status.lower(), status)


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
def build_snippets_section(engine_slug, engine_ref, shots) -> str:
    snippets = sorted(SNIPPETS_DIR.glob("[0-9]*.py"))
    parsed = [parse_snippet(p) for p in snippets]

    out = []
    out.append("## Playground Snippets\n")
    out.append(
        f"{len(parsed)} focused, copy-paste examples covering the whole "
        "`mcrfpy` API. Each snippet fills the 1024x768 playground canvas.\n")
    out.append(
        "> **Open in playground:** the "
        "[playground]({{ site.baseurl }}/playground/) accepts shared code via "
        "an LZString-compressed `#src=` URL fragment or a `#gist=` id, but "
        "there is **no by-URL loader** to open a repo snippet directly. Copy "
        "the source below and paste it into the editor, then press Run "
        "(Ctrl+Enter).\n")

    if engine_slug is None:
        out.append("_(Could not resolve a github.com remote for the engine "
                   "repo; source links omitted.)_\n")

    # Group by leading category token, preserving first-seen order.
    groups: dict[str, list] = {}
    for info in parsed:
        groups.setdefault(category_from_stem(info["stem"]), []).append(info)

    for cat, items in groups.items():
        out.append(f"\n### {cat.replace('_', ' ').title()}\n")
        out.append("| # | Snippet | Preview | Objects | Status | Source |")
        out.append("|---|---------|---------|---------|--------|--------|")
        for info in items:
            title = info["title"]
            if info["desc"]:
                title = f"**{title}**<br><span style=\"color:#888\">" \
                        f"{info['desc']}</span>"
            objs = ", ".join(f"`{o}`" for o in info["objects"]) or "&mdash;"
            badge = status_badge(info["status"])
            if info["stem"] in shots:
                src = f"{{{{ site.baseurl }}}}{SNIPPET_SHOTS_WEB}/{info['stem']}.png"
                preview = (f'<img src="{src}" alt="{info["title"]} preview" '
                           f'loading="lazy" width="220">')
            else:
                preview = "&mdash;"
            if engine_slug:
                rel = f"tests/snippets/{info['stem']}.py"
                link = f"[view]({blob_url(engine_slug, engine_ref, rel)}) &middot; " \
                       f"[raw]({raw_url(engine_slug, engine_ref, rel)})"
            else:
                link = "&mdash;"
            out.append(f"| {info['number']} | {title} | {preview} | {objs} | "
                       f"{badge} | {link} |")
        out.append("")

    return "\n".join(out)


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

    LIBRARY_DIR.mkdir(parents=True, exist_ok=True)

    shots = sync_snippet_shots()
    snippets_md = build_snippets_section(engine_slug, engine_ref, shots)
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
        "**games**. Source links are pinned to specific commits so they keep "
        "working as the code evolves.\n")
    page.append(
        f"<sub>Snippets pinned to site `{site_ref}`"
        + (f" ([{site_slug}](https://github.com/{site_slug}))" if site_slug else "")
        + f"; demos/games pinned to engine `{engine_ref}`"
        + (f" ([{engine_slug}](https://github.com/{engine_slug}))" if engine_slug else "")
        + ". Generated by `tools/build_library.py`.</sub>\n")
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
    print(f"  snippets:    {len(sorted(SNIPPETS_DIR.glob('[0-9]*.py')))} "
          f"({len(shots)} with previews -> {SNIPPET_SHOTS_DST})")
    print(f"  demo screens: {demo_stats['screens']} "
          f"(thumbnails {demo_stats['available']} available / "
          f"{demo_stats['missing']} missing)")
    print(f"  games:       {len(games)} -> {games}")
    print(f"  wrote: {index_path}")
    print(f"  wrote: {todo_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
