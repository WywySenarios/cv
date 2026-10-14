#!/usr/bin/env bash
# Create applications/<slug>/jd.md for a new application.
# Usage: scripts/new-application.sh <slug>
set -euo pipefail

if [ "$#" -ne 1 ]; then
	echo "usage: new-application.sh <slug>" >&2
	exit 2
fi

slug="$1"
root="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$root/applications/$slug"
touch "$root/applications/$slug/jd.md"
printf 'created %s\n' "$root/applications/$slug/jd.md"
