#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p sc26_outputs
python sc26_artifact/verify_repository.py | tee sc26_outputs/preflight.log
python sc26_artifact/verify_reference_results.py | tee sc26_outputs/reference_output_verification.log
python paper_figures/generate_paper_figures.py --output-dir sc26_outputs/paper_figures | tee sc26_outputs/figure_generation.log
printf 'Quick check complete. Outputs are in %s\n' "$ROOT/sc26_outputs"
