# rareHPC

**Archived release:** https://doi.org/10.5281/zenodo.21439797

`rareHPC` runs the held-out evaluation pipeline for the paper **RARE-HPC: Risk-Aware Resource Recommendations for Memory and Wall-Time Requests on a Production HPC Cluster**. The repository contains the processed one-week test trace, fitted encoders, model-download support, the inference and recommendation code, automated result checks, and the data and scripts used to recreate the paper figures.


## What the public artifact evaluates

The public workflow performs the following steps:

1. validates the processed held-out trace and repository structure;
2. obtains the released LightGBM selective-gate model and two Random Forest utilization models;
3. runs the memory and wall-time recommendation branches;
4. converts predictions into direct and safer bucketed recommendations;
5. checks the held-out metrics against the released reference values; and
6. recreates all eight paper figures from the distributed numerical inputs.

The public trace covers 17-24 January 2024. It contains 26,591 processed jobs from 109 encoded users and 25 account labels. The history-eligibility rule used by the executable pipeline retains 24,461 jobs associated with four eligible user histories and four account labels.

## Installation

A Linux x86-64 workstation with at least four CPU cores, 16 GB RAM, 5 GB free disk space, and outbound HTTPS access is recommended. The workflow does not require a GPU, Slurm installation, or access to the Jubail cluster.

```bash
git clone https://github.com/NYUAD-CRC/rareHPC.git
cd rareHPC
conda env create -f environment.yml
conda activate rareHPC
python -m pip install -r requirements.txt
plotly_get_chrome -y
```

A compatible Chrome or Chromium installation can be used instead of `plotly_get_chrome`.

## Quick validation

The quick check does not download or execute the trained models. It validates the trace, verifies the numerical values encoded in the distributed output matrices and account summaries, and recreates the eight paper figures.

```bash
bash sc26_artifact/run_quickcheck.sh
```

Outputs are written to `sc26_outputs/`.

## Full held-out evaluation

```bash
bash sc26_artifact/run_ae.sh
```

The wrapper downloads any missing model files from the public `v1.0` release, runs both recommendation branches, checks the resulting logs, and regenerates the paper figures.

The two original inference commands remain available:

```bash
python test.py --y "memory_efficiency_%"
python test.py --y "%_UtilisedTime"
```

## Expected executable results

The released held-out pipeline should produce the following values, subject to the tolerances in `sc26_artifact/expected_results.json`.

| Output | Accuracy | Recall | Precision |
|---|---:|---:|---:|
| Selective gate | 94.47% | 96.40% | 91.53% |

| Branch | Weighted recall | Weighted precision | Under-provisioning | Direct reduction | Safer reduction |
|---|---:|---:|---:|---:|---:|
| Memory | 60.97% | 80.65% | 2.00% | 73.00% | 44.50% |
| Wall time | 84.15% | 97.71% | 0.44% | 80.00% | 66.50% |

The paper also distributes the exact frozen aggregate values used in its final tables and figures. Those files are kept under `paper_figures/data/` and are regenerated separately from the executable test output.

## Recreating the paper figures

```bash
python paper_figures/generate_paper_figures.py \
  --output-dir sc26_outputs/paper_figures
```

The script creates PDF, PNG, and SVG versions of Figs. 1-8. The reference files used by the submitted manuscript are stored in `paper_figures/reference/`.

## Data availability and privacy

The approximately 2.1-million-job development trace is not distributed. It was collected from the NYU Abu Dhabi production HPC service and contains operational fields that can be identifying when combined, including user and project membership, job names, precise submission and execution times, partition and quality-of-service information, resource requests, and observed consumption. These records can reveal research activity, workload schedules, and recurring project behavior even after direct names are removed. The trace has not been approved for public release under the operational-data governance applied by the NYUAD HPC team.

The repository includes `DataPreprocess.ipynb` and `train.py` so that the preprocessing, feature engineering, temporal splitting, sampling, and model-training logic can be inspected. Public execution uses the processed held-out trace, released encoders and models, and de-identified aggregate inputs for the paper figures.

## Repository layout

- `test.py`: held-out selective-gate and recommendation pipeline;
- `train.py`: model-training and model-selection code;
- `DataPreprocess.ipynb`: preprocessing and feature construction;
- `test.csv`: processed held-out trace;
- `download_models.py`: downloads the released pretrained models;
- `sc26_artifact/`: validation, execution, and result-checking scripts;
- `paper_figures/`: figure-generation code, numerical inputs, and reference figures.

## Citation

```bibtex
@software{mannem_rareHPC_2026,
  author    = {Mannem, Karunakar Reddy and Jhala, Dhanu Vardhan Singh and
               Zia, Waqqas and Saleh, Mennatallah Samier and
               Al Barwani, Muataz},
  title     = {rareHPC: Risk-Aware Resource Recommendation Test Pipeline for Production HPC},
  year      = {2026},
  version   = {1.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.21439797},
  url       = {https://doi.org/10.5281/zenodo.21439797}
}
```
