#!/usr/bin/env python3
"""Fix common API issues in playground snippets."""
import os
import re

SNIPPETS_DIR = "/home/john/Development/mcrogueface.github.io/snippets"

def fix_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    original = content

    # Fix 1: tile_index -> tilesprite
    content = re.sub(r'\.tile_index\b', '.tilesprite', content)

    # Fix 2: Caption color kwarg - move to fill_color after creation
    # This is complex, skip for now

    # Fix 3: Key.Num1 -> Key.NUM_1 etc
    content = re.sub(r'Key\.Num(\d)', r'Key.NUM_\1', content)

    # Fix 4: FOV.PERMISSIVE4 -> FOV.PERMISSIVE_4
    content = re.sub(r'FOV\.PERMISSIVE(\d)', r'FOV.PERMISSIVE_\1', content)

    # Fix 5: .magnitude format -> .magnitude()
    content = re.sub(r'v(\d*)\.magnitude(?!\()', r'v\1.magnitude()', content)

    # Fix 6: global_pos -> global_bounds (or remove)
    content = content.replace('.global_pos', '.global_bounds')

    # Fix 7: cell.color -> needs color layer (complex, skip)

    # Fix 8: cell.visible -> different API

    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    changed = 0
    for fname in sorted(os.listdir(SNIPPETS_DIR)):
        if fname.endswith('.py'):
            filepath = os.path.join(SNIPPETS_DIR, fname)
            if fix_file(filepath):
                print(f"Fixed: {fname}")
                changed += 1
    print(f"\nFixed {changed} files")

if __name__ == "__main__":
    main()
