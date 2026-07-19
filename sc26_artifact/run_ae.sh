#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p sc26_outputs
export MPLBACKEND=Agg

{
  date -u +"UTC start: %Y-%m-%dT%H:%M:%SZ"
  python --version
  python -m pip --version
} | tee sc26_outputs/environment.log

python sc26_artifact/verify_repository.py | tee sc26_outputs/preflight_before_models.log

if [ ! -s classification_model/models/ClassFier_LGBM_alldata.joblib ] || \
   [ ! -s MEMwithsampling/models/RandomForest_balanced_all_MEMwithsampling.joblib ] || \
   [ ! -s ComputeTimewithsampling/models/RandomForest_balanced_all_ComputeTimewithsampling.joblib ]; then
  echo "Downloading pretrained models from the public rareHPC v1.0 release."
  python download_models.py
fi

python sc26_artifact/verify_repository.py --require-models | tee sc26_outputs/preflight_after_models.log
python sc26_artifact/verify_reference_results.py | tee sc26_outputs/reference_output_verification.log
python test.py --y "memory_efficiency_%" 2>&1 | tee sc26_outputs/memory.log
python test.py --y "%_UtilisedTime" 2>&1 | tee sc26_outputs/walltime.log
python sc26_artifact/verify_outputs.py \
  --memory-log sc26_outputs/memory.log \
  --walltime-log sc26_outputs/walltime.log | tee sc26_outputs/verification.log
python paper_figures/generate_paper_figures.py --output-dir sc26_outputs/paper_figures | tee sc26_outputs/figure_generation.log

date -u +"UTC end: %Y-%m-%dT%H:%M:%SZ" | tee -a sc26_outputs/environment.log
echo "Artifact evaluation workflow completed."
echo "Inspect sc26_outputs/verification.log and sc26_outputs/paper_figures/."
