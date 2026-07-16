#!/usr/bin/env python3
"""Verify tools/lzstring.py against the real lz-string npm library via node.

Compresses every engine snippet (and a few tricky literals) with our pure-python
port, hands the tokens to node's lz-string decoder, and asserts the decoded
sha256 matches the original source's sha256. A mismatch means our port diverged
from the library the deployed playground actually runs.
"""
import hashlib
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from lzstring import compress_to_encoded_uri_component  # noqa: E402

HERE = Path(__file__).parent
ENGINE_ROOT = Path(
    os.environ.get("ENGINE_ROOT", HERE.parent.parent / "McRogueFace")
)
SNIPPETS = ENGINE_ROOT / "tests" / "snippets"
# lz-string is not a site dependency; borrow a cached copy for the test only.
NODE_MODULES = Path(
    "/home/john/Development/protoforge/app/client/node_modules"
)


def sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def main() -> int:
    samples = []  # (label, source)
    for p in sorted(SNIPPETS.glob("[0-9]*.py")):
        samples.append((p.name, p.read_text(encoding="utf-8")))
    # Edge cases: empty, unicode above U+00FF, repeated runs, lone chars.
    samples += [
        ("<empty>", ""),
        ("<unicode>", "grid = '★ ▲ ✦'  # entities\nx = 'café'\n"),
        ("<repeat>", "a" * 500),
        ("<single>", "x"),
    ]

    tokens = [compress_to_encoded_uri_component(src) for _, src in samples]

    env = dict(os.environ, NODE_PATH=str(NODE_MODULES))
    proc = subprocess.run(
        ["node", str(HERE / "test_lzstring.js"), *tokens],
        capture_output=True, text=True, env=env,
    )
    if proc.returncode != 0:
        print("node decoder failed:", proc.stderr, file=sys.stderr)
        return 2

    got = proc.stdout.strip().split("\n")
    if len(got) != len(samples):
        print(f"expected {len(samples)} hashes, got {len(got)}", file=sys.stderr)
        return 2

    fails = 0
    for (label, src), decoded_hash in zip(samples, got):
        if decoded_hash != sha(src):
            fails += 1
            print(f"MISMATCH: {label}")
    if fails:
        print(f"\n{fails}/{len(samples)} round-trips FAILED")
        return 1
    print(f"PASS: {len(samples)} round-trips match lz-string@1.5.0 decode")
    return 0


if __name__ == "__main__":
    sys.exit(main())
