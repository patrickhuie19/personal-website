#!/usr/bin/env bash
# Run all analysis scripts that feed the static site (charts + data exports).
# Vercel and other CI environments do not install Python chart deps; committed
# assets under public/assets/ and data/ are used as-is. Regenerate locally before push.
set -euo pipefail
cd "$(dirname "$0")/../.."

if [ -n "${SKIP_ANALYZE:-}" ]; then
  echo "SKIP_ANALYZE set: skipping chart generation." >&2
  exit 0
fi

if [ -n "${VERCEL:-}" ] || [ "${CI:-}" = "true" ]; then
  echo "Vercel/CI: skipping Python chart generation (using committed SVGs and CSVs)." >&2
  exit 0
fi

python3 scripts/analysis/economics-of-local-llms.py
