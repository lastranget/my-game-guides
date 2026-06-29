#!/usr/bin/env bash
# Fetch a GameFAQs FAQ as raw text via the Wayback Machine.
# GameFAQs is Cloudflare-walled (curl/WebFetch/headless-Chromium all get the
# "Just a moment…" challenge), but archive.org mirrors the FAQ text and is open.
#
# Usage: tools/kof_fetch.sh <platform/gameid-slug> <faq-id> [outfile.html]
#   e.g. tools/kof_fetch.sh arcade/928580-the-king-of-fighters-xi 44141 raw.html
# Then run: python3 tools/kof_convert.py extract raw.html > faq.txt
set -euo pipefail
SLUG="$1"; FAQ="$2"; OUT="${3:-faq-$FAQ.html}"
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
URL="gamefaqs.gamespot.com/${SLUG}/faqs/${FAQ}"
TS=$(curl -s "https://archive.org/wayback/available?url=${URL}" \
  | python3 -c "import sys,json;s=json.load(sys.stdin)['archived_snapshots'].get('closest');print(s['timestamp'] if s else '')")
[ -z "$TS" ] && { echo "no Wayback snapshot for $URL" >&2; exit 1; }
# the 'id_' after the timestamp returns the RAW archived page (no Wayback toolbar)
curl -s -A "$UA" -o "$OUT" "http://web.archive.org/web/${TS}id_/https://${URL}"
echo "saved $OUT ($(wc -c <"$OUT") bytes) from snapshot $TS"
