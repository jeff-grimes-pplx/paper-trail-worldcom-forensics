#!/usr/bin/env bash
# Copy the built dataset into the deployable app folder (app/data). Run after any rebuild.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p app/data
for f in register.json ledger.json series.json timeline.json pdf-highlights.json pagecounts.json SHA256SUMS.txt verification.json; do
  [ -f "data/$f" ] && cp "data/$f" "app/data/$f"
done
rsync -a --delete data/pages/ app/data/pages/
rsync -a --delete data/pdf-pages/ app/data/pdf-pages/
rsync -a --delete data/edgar-img/ app/data/edgar-img/
du -sh app/data
