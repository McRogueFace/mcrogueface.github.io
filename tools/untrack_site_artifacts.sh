#!/usr/bin/env bash
#
# untrack_site_artifacts.sh -- stop tracking Jekyll build artifacts that are
# now gitignored (_site/ and .jekyll-cache/). This removes them from the git
# index only; your working-tree files are left untouched.
#
# Run from anywhere. By default this is a DRY RUN and only prints what it
# would do. Pass --apply to actually run `git rm -r --cached`.
#
#   ./tools/untrack_site_artifacts.sh           # dry run (safe)
#   ./tools/untrack_site_artifacts.sh --apply    # actually untrack
#
# After --apply, review and commit:
#   git status
#   git commit -m "chore: stop tracking Jekyll build artifacts"
#
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

PATHS=("_site" ".jekyll-cache")

APPLY=0
if [[ "${1:-}" == "--apply" ]]; then
    APPLY=1
elif [[ -n "${1:-}" ]]; then
    echo "Unknown argument: $1" >&2
    echo "Usage: $0 [--apply]" >&2
    exit 2
fi

echo "Repository: $REPO_ROOT"
echo

any_tracked=0
for p in "${PATHS[@]}"; do
    # List index entries under this path (if any).
    if git ls-files --error-unmatch "$p" >/dev/null 2>&1 || \
       [[ -n "$(git ls-files -- "$p")" ]]; then
        count="$(git ls-files -- "$p" | wc -l | tr -d ' ')"
        if [[ "$count" -gt 0 ]]; then
            any_tracked=1
            echo "Tracked under '$p': $count file(s)"
            if [[ "$APPLY" -eq 1 ]]; then
                git rm -r --cached --quiet -- "$p"
                echo "  -> git rm -r --cached -- $p   (done)"
            else
                echo "  -> would run: git rm -r --cached -- $p"
            fi
        fi
    fi
done

if [[ "$any_tracked" -eq 0 ]]; then
    echo "Nothing to untrack -- neither _site/ nor .jekyll-cache/ is tracked."
    exit 0
fi

echo
if [[ "$APPLY" -eq 1 ]]; then
    echo "Untracked. Review with 'git status' and commit when ready."
else
    echo "Dry run only. Re-run with --apply to actually untrack."
fi
