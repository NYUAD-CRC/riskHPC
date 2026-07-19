# Training-data privacy and artifact scope

## Protected development trace

The models and development-period analyses in the paper were produced from approximately 2.1 million Slurm accounting records collected on the NYU Abu Dhabi production HPC service between 28 June 2023 and 17 January 2024. These records are operational service data rather than a research dataset collected for public release.

The trace contains fields that can remain identifying when considered together: persistent user and project membership, job names, exact submission and execution times, partition and quality-of-service settings, resource requests, and observed memory and runtime. Such combinations can reveal active research projects, computational campaign schedules, recurring application patterns, and individual or laboratory usage. Replacing direct names does not remove the linkage risk created by timestamps, account membership, job names, and repeated workflows.

Public distribution of the raw development trace has not been approved under the operational-data governance applied by the NYUAD HPC team. The archive therefore does not contain the individual production records used for preprocessing, feature engineering, model training, model selection, or development-split evaluation.

## Publicly distributed material

The archive provides the components needed to inspect the method and evaluate the released held-out pipeline:

- `DataPreprocess.ipynb` and `train.py`, which expose the preprocessing, rolling-feature, sampling, and training logic;
- a processed one-week held-out trace with encoded identifiers;
- fitted encoders and access to released pretrained models;
- the public memory and wall-time inference pipeline;
- machine-readable expected outputs and verification scripts;
- de-identified aggregate values used by the paper figures; and
- Python code that recreates all eight paper figures.

The processed public trace spans 17-24 January 2024. It contains 26,591 rows, 109 encoded user identifiers, and 25 account labels. The history-eligibility rule implemented by `test.py` retains 24,461 rows associated with four eligible user histories and four account labels for model evaluation.

## Interpretation of reproducibility

The public archive supports functional evaluation of the released recommendation pipeline and exact regeneration of the figures from their distributed numerical inputs. Full retraining and independent recomputation of development-period statistics require authorized access to the protected production trace. This distinction is stated explicitly in the accompanying Artifact Description and Artifact Evaluation appendix.
