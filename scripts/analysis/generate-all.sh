#!/usr/bin/env bash
# Run all analysis scripts that feed the static site (charts + data exports).
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 scripts/analysis/economics-of-local-llms.py
