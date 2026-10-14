#!/usr/bin/env bash
# assemble resume.tex, then compile it to PDF.
# Usage: scripts/build.sh <slug>
set -euo pipefail

slug="${1:?usage: build.sh <slug>}"
root="$(cd "$(dirname "$0")/.." && pwd)"

export PATH="$HOME/Library/TinyTeX/bin/universal-darwin:$PATH"

cd "$root"
uv run python scripts/assemble.py "$slug"

export TEXINPUTS="$root/templates:"

cd "applications/$slug"
xelatex -interaction=nonstopmode -halt-on-error resume.tex

# xelatex records the page count in the log; no extra tooling needed.
pages="$(grep -oE 'Output written on [^(]+\([0-9]+ page' resume.log | grep -oE '[0-9]+' | tail -1 || true)"

printf '\nbuilt %s' "$root/applications/$slug/resume.pdf"
if [ -n "$pages" ]; then
	plural=''
	[ "$pages" -eq 1 ] || plural='s'
	printf ' (%s page%s)' "$pages" "$plural"
fi
printf '\n'

if [ -n "$pages" ] && [ "$pages" -gt 1 ]; then
	printf 'warning: %s pages; target is 1. Trim atoms or tighten the select-atoms budget.\n' "$pages" >&2
fi
