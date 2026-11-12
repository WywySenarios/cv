#!/usr/bin/env bash
# assemble and compile a resume and/or cover letter to PDF.
# Usage: scripts/build.sh <slug> [resume|letter|both]   (default: resume)
set -euo pipefail

slug="${1:?usage: build.sh <slug> [resume|letter|both]}"
target="${2:-resume}"

root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"

export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"
export TEXINPUTS="$root/templates:"

# target -> document basename(s). The letter's file is cover-letter.tex.
case "$target" in
resume) docs=(resume) ;;
letter) docs=(cover-letter) ;;
both) docs=(resume cover-letter) ;;
*)
	printf 'unknown target: %s (expected resume, letter, or both)\n' "$target" >&2
	exit 2
	;;
esac

for doc in "${docs[@]}"; do
	case "$doc" in
	resume) uv run python scripts/assemble.py "$slug" ;;
	cover-letter) uv run python scripts/assemble-letter.py "$slug" ;;
	esac

	(cd "applications/$slug" && xelatex -interaction=nonstopmode -halt-on-error "$doc.tex")

	# xelatex records the page count in the log; no extra tooling needed.
	pages="$(grep -oE 'Output written on [^(]+\([0-9]+ page' "applications/$slug/$doc.log" | grep -oE '[0-9]+' | tail -1 || true)"

	printf '\nbuilt %s' "$root/applications/$slug/$doc.pdf"
	if [ -n "$pages" ]; then
		plural=''
		[ "$pages" -eq 1 ] || plural='s'
		printf ' (%s page%s)' "$pages" "$plural"
	fi
	printf '\n'

	if [ -n "$pages" ] && [ "$pages" -gt 1 ]; then
		printf 'warning: %s is %s pages; target is 1.\n' "$doc" "$pages" >&2
	fi
done
