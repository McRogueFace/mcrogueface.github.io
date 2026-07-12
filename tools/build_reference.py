#!/usr/bin/env python3
"""Generate the McRogueFace API *reference* pages from engine-emitted JSON.

This builder consumes two deterministic artifacts produced by the engine build:

  * api/manifest.json        -- structural manifest: objects, members, kinds,
                                signatures, doc_sha hashes, and per-symbol
                                lifecycle metadata (since / modified /
                                deprecated / removed).
  * docs/generated/api_full.json -- the same symbols carrying their full
                                docstring text ("doc").

For every class it writes ``reference/generated/<Name>.md`` and it collects all
module-level functions into ``reference/generated/functions.md``. It also drops
``_data/mcrf_api.yml`` with the manifest's {version, commit} so templates and
the sidebar can surface "verified against" provenance.

Design constraints (see the docs-site task brief):

  * stdlib only, plain python3;
  * deterministic + idempotent -- re-running with the same inputs yields
    byte-identical output, and stale generated pages are pruned first;
  * docstrings are UNTRUSTED plain text. They are wrapped in Liquid ``{% raw %}``
    guards (with the ``{% endraw %}`` escape vector neutralized) so a docstring
    can never inject Liquid/Jekyll markup into the rendered site.

IMPORTANT -- PARALLEL TREE, NOT A CUTOVER:
  ``reference/generated/`` is a *new* tree that runs ALONGSIDE the hand-written
  ``objects/*.md`` pages. Nothing here overwrites or redirects the curated
  pages. Whether (and how) the generated tree replaces the hand-written one is a
  deliberate future decision, out of scope for this script. Until then both
  trees coexist; only ``reference/generated/**`` and ``_data/mcrf_api.yml`` are
  owned by this tool.
"""

import argparse
import json
import os
import re
import sys

# Repo root = parent of this tools/ directory.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_MANIFEST = os.path.join(REPO_ROOT, "..", "McRogueFace", "api", "manifest.json")
DEFAULT_FULL = os.path.join(REPO_ROOT, "..", "McRogueFace", "docs", "generated", "api_full.json")
DEFAULT_OUT = os.path.join(REPO_ROOT, "reference", "generated")
DATA_FILE = os.path.join(REPO_ROOT, "_data", "mcrf_api.yml")

BADGE = 'api_badge.html'

# Members whose kind puts them in the "Properties" table vs the "Methods" list.
PROPERTY_KINDS = {"property"}
METHOD_KINDS = {"method", "classmethod", "staticmethod"}


# --------------------------------------------------------------------------- #
# Liquid / Jekyll safety
# --------------------------------------------------------------------------- #

# Matches a Liquid raw-close tag with the flexible whitespace Liquid allows,
# e.g. "{% endraw %}", "{%- endraw -%}", "{%endraw%}". We only need to defang
# the opening "{%" of such a sequence so it cannot terminate OUR raw block.
_RAW_CLOSE = re.compile(r"\{%(-?\s*endraw\s*-?)%\}")


def liquid_raw(text):
    """Wrap untrusted ``text`` so Liquid emits it verbatim.

    ``{% raw %}...{% endraw %}`` tells Liquid to skip tag/output processing for
    the enclosed span, which neutralizes ``{{ ... }}`` and ``{% ... %}`` that
    may legitimately appear inside example code in a docstring. The one escape
    vector -- a docstring literally containing ``{% endraw %}`` -- is defanged
    by breaking the opening brace pair of any such close tag first.
    """
    if not text:
        return ""
    safe = _RAW_CLOSE.sub(r"{ %\1%}", text)
    return "{% raw %}" + safe + "{% endraw %}"


def liquid_cell(text):
    """Liquid- and table-safe single-line rendering for a Markdown table cell.

    Collapses newlines, escapes pipes (which would break the table), then
    applies the same raw-guard as :func:`liquid_raw`.
    """
    if not text:
        return ""
    first = text.strip().splitlines()
    line = first[0] if first else ""
    line = line.replace("|", "\\|")
    return liquid_raw(line)


# --------------------------------------------------------------------------- #
# Lifecycle -> badges
# --------------------------------------------------------------------------- #

def badge(kind, version=None, note=None):
    """Emit a Liquid include call for one lifecycle badge."""
    parts = ['{%% include %s kind="%s"' % (BADGE, kind)]
    if version:
        parts.append('version="%s"' % _attr(version))
    if note:
        parts.append('note="%s"' % _attr(note))
    parts.append("%}")
    return " ".join(parts)


def _attr(value):
    """Sanitize a value destined for a double-quoted Liquid include argument."""
    return str(value).replace("\\", "").replace('"', "'").replace("\n", " ")


def lifecycle_badges(lifecycle, baseline):
    """Return the ordered list of badge include-strings for a lifecycle dict.

    ``baseline`` is the seeded manifest version; symbols whose ``since`` equals
    the baseline are considered "always been here" and get no 'added' badge.
    Unknown/future lifecycle keys are ignored gracefully; the renderer only
    reacts to since/modified/deprecated/removed.
    """
    if not lifecycle:
        return []
    out = []
    since = lifecycle.get("since")
    if since and since != baseline:
        out.append(badge("added", since))
    modified = lifecycle.get("modified")
    if isinstance(modified, dict) and modified.get("version"):
        out.append(badge("changed", modified.get("version")))
    deprecated = lifecycle.get("deprecated")
    if isinstance(deprecated, dict) and deprecated.get("version"):
        out.append(badge("deprecated", deprecated.get("version"), deprecated.get("note")))
    removed = lifecycle.get("removed")
    if isinstance(removed, dict) and removed.get("version"):
        out.append(badge("removed", removed.get("version"), removed.get("note")))
    return out


# --------------------------------------------------------------------------- #
# Rendering
# --------------------------------------------------------------------------- #

def frontmatter(name, version, commit):
    """Emit YAML frontmatter (hand-built; stdlib only, no yaml dep)."""
    lines = [
        "---",
        "title: %s" % _yaml_scalar(name),
        "layout: default",
        "mcrf:",
        "  objects:",
        "    - %s" % _yaml_scalar(name),
        "  diataxis: reference",
        "  source: generated",
        "  verified: %s" % _yaml_scalar(version),
        "  verified_commit: %s" % _yaml_scalar(commit),
        "---",
    ]
    return "\n".join(lines)


def _yaml_scalar(value):
    """Quote a scalar for YAML when it could be misparsed; otherwise plain."""
    s = "" if value is None else str(value)
    if s == "" or s[0] in "!&*?|>%@`\"'#-[]{}," or ":" in s or "#" in s:
        return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')
    return s


def render_signature(name, sig):
    """Produce the display call-signature for ``name`` given its raw ``sig``.

    Two signature encodings are tolerated because the schema-by-example and the
    engine's actual emitter disagree:

      * bare parameter list, e.g. ``"(n=1, turn_order=None)"`` -- the documented
        schema. The member name is prepended: ``name(n=1, turn_order=None)``.
      * fully-qualified, e.g. ``"pause() -> None"`` or
        ``"animate(prop, ...) -> Animation"`` -- what the engine actually emits.
        It already carries the name (and any return annotation), so it is used
        verbatim to avoid a doubled name (``pausepause()``).

    Empty ``sig`` (properties, or a name with no recorded params) yields
    ``name()``.
    """
    s = (sig or "").strip()
    if not s:
        return "%s()" % name
    if s[0] == "(":
        return "%s%s" % (name, s)
    return s


def compute_baseline(manifest):
    """Infer the seeded-baseline version: the version most symbols were stamped
    at.

    The manifest carries a (possibly ``-dev``) working ``version`` that need not
    equal the version the API surface was seeded at -- e.g. version
    ``"0.2.8-dev"`` while every seeded symbol has ``since: "0.2.8"``. Using the
    working version as the baseline would tag every symbol as newly "added".

    Instead the baseline is the modal ``since`` value across all objects,
    members, and functions: seeding stamps the bulk of the surface with one
    version, so the most common ``since`` is that seed. Symbols added later have
    a rarer, newer ``since`` and correctly earn an "added" badge. Ties break
    lexically for determinism. Falls back to the manifest ``version`` when no
    lifecycle data is present.
    """
    counts = {}

    def tally(lifecycle):
        if not lifecycle:
            return
        since = lifecycle.get("since")
        if since:
            counts[since] = counts.get(since, 0) + 1

    for obj in (manifest.get("objects") or {}).values():
        tally(obj.get("lifecycle"))
        for member in (obj.get("members") or {}).values():
            tally(member.get("lifecycle"))
    for fn in (manifest.get("functions") or {}).values():
        tally(fn.get("lifecycle"))

    if not counts:
        return manifest.get("version")
    # max count, then lexically-smallest version as a deterministic tie-break.
    return max(sorted(counts), key=lambda v: counts[v])


def render_object(name, obj, full_obj, baseline, version, commit):
    doc = (full_obj or {}).get("doc", "")
    members = obj.get("members", {}) or {}
    full_members = (full_obj or {}).get("members", {}) or {}

    out = [frontmatter(name, version, commit), ""]

    # Title + class-level lifecycle badges.
    badges = lifecycle_badges(obj.get("lifecycle"), baseline)
    heading = "# %s" % name
    if badges:
        heading += " " + " ".join(badges)
    out.append(heading)
    out.append("")

    # Class docstring (untrusted).
    if doc:
        out.append(liquid_raw(doc))
        out.append("")

    # Split members deterministically by kind.
    props = sorted((k, v) for k, v in members.items() if v.get("kind") in PROPERTY_KINDS)
    methods = sorted((k, v) for k, v in members.items() if v.get("kind") in METHOD_KINDS)
    other = sorted((k, v) for k, v in members.items()
                   if v.get("kind") not in PROPERTY_KINDS and v.get("kind") not in METHOD_KINDS)
    # Unknown member kinds are surfaced as methods rather than dropped.
    methods = sorted(methods + other)

    if props:
        out.append("## Properties")
        out.append("")
        out.append("| Property | Description |")
        out.append("| --- | --- |")
        for mname, m in props:
            mbadges = lifecycle_badges(m.get("lifecycle"), baseline)
            cell_name = "`%s`" % mname
            if mbadges:
                cell_name += " " + " ".join(mbadges)
            desc = liquid_cell((full_members.get(mname) or {}).get("doc", ""))
            out.append("| %s | %s |" % (cell_name, desc))
        out.append("")

    if methods:
        out.append("## Methods")
        out.append("")
        for mname, m in methods:
            kind = m.get("kind", "method")
            mbadges = lifecycle_badges(m.get("lifecycle"), baseline)
            mheading = "### `%s`" % render_signature(mname, m.get("signature"))
            if mbadges:
                mheading += " " + " ".join(mbadges)
            out.append(mheading)
            out.append("")
            if kind in ("classmethod", "staticmethod"):
                out.append("*%s*" % kind)
                out.append("")
            mdoc = (full_members.get(mname) or {}).get("doc", "")
            if mdoc:
                out.append(liquid_raw(mdoc))
                out.append("")

    return "\n".join(out).rstrip() + "\n"


def render_functions(functions, full_functions, baseline, version, commit):
    out = [frontmatter("Module Functions", version, commit), ""]
    out.append("# Module Functions")
    out.append("")
    out.append("Top-level functions in the `mcrfpy` module.")
    out.append("")
    for fname, f in sorted(functions.items()):
        fbadges = lifecycle_badges(f.get("lifecycle"), baseline)
        heading = "## `mcrfpy.%s`" % render_signature(fname, f.get("signature"))
        if fbadges:
            heading += " " + " ".join(fbadges)
        out.append(heading)
        out.append("")
        fdoc = (full_functions.get(fname) or {}).get("doc", "")
        if fdoc:
            out.append(liquid_raw(fdoc))
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def render_data(version, commit):
    return (
        "# Generated by tools/build_reference.py -- do not edit by hand.\n"
        "version: %s\n"
        "commit: %s\n"
    ) % (_yaml_scalar(version), _yaml_scalar(commit))


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #

def load_json(path, what):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        sys.stderr.write("error: %s not found: %s\n" % (what, path))
        sys.exit(2)
    except json.JSONDecodeError as exc:
        sys.stderr.write("error: %s is not valid JSON: %s\n" % (what, exc))
        sys.exit(2)


def write_if_changed(path, content):
    """Write only when content differs; returns 'created'|'updated'|'unchanged'."""
    existing = None
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            existing = fh.read()
    if existing == content:
        return "unchanged"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    return "created" if existing is None else "updated"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the generated API reference pages.")
    ap.add_argument("--manifest", default=DEFAULT_MANIFEST, help="path to api/manifest.json")
    ap.add_argument("--full", default=DEFAULT_FULL, help="path to docs/generated/api_full.json")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output dir for generated reference pages")
    args = ap.parse_args(argv)

    manifest = load_json(args.manifest, "manifest")
    full = load_json(args.full, "api_full")

    version = manifest.get("version", "unknown")
    commit = manifest.get("commit", "unknown")
    # Seeded baseline is inferred from the lifecycle data, not the working
    # version -- see compute_baseline (e.g. version "0.2.8-dev" but seed
    # "0.2.8").
    baseline = compute_baseline(manifest) or version

    objects = manifest.get("objects", {}) or {}
    functions = manifest.get("functions", {}) or {}
    full_objects = full.get("objects", {}) or {}
    full_functions = full.get("functions", {}) or {}

    os.makedirs(args.out, exist_ok=True)

    # Determine the exact set of files we intend to own this run.
    expected = {"functions.md"}
    for name in objects:
        expected.add("%s.md" % name)

    # Prune stale generated pages so the tree is deterministic across renames.
    for existing in os.listdir(args.out):
        if existing.endswith(".md") and existing not in expected:
            os.remove(os.path.join(args.out, existing))

    created = []
    for name in sorted(objects):
        page = render_object(name, objects[name], full_objects.get(name),
                             baseline, version, commit)
        path = os.path.join(args.out, "%s.md" % name)
        write_if_changed(path, page)
        created.append(path)

    fpath = os.path.join(args.out, "functions.md")
    write_if_changed(fpath, render_functions(functions, full_functions, baseline, version, commit))
    created.append(fpath)

    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    write_if_changed(DATA_FILE, render_data(version, commit))
    created.append(DATA_FILE)

    sys.stderr.write("build_reference: %d object pages + functions.md, verified %s (%s)\n"
                     % (len(objects), version, commit))
    for p in created:
        sys.stderr.write("  %s\n" % p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
