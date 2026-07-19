# Artifact validation report

The archived artifact was checked against the supplied repository snapshot and the numerical outputs distributed with the public test pipeline.

## Completed checks

- repository-file and environment inventory;
- processed-trace schema, row count, encoded-user count, account count, and date range;
- history-eligibility subset count;
- presence of the three fitted encoders;
- presence of eight reference manuscript figures;
- exact reconstruction of the selective-gate metrics from the distributed confusion matrix;
- exact reconstruction of memory and wall-time weighted recall, weighted precision, and under-provisioning from the distributed bucket confusion matrices;
- exact reconstruction of account-mean direct and safer reductions from the distributed held-out account summaries; and
- recreation of all eight manuscript figures in PDF, PNG, and SVG formats.

## Verified public-output values

| Output | Value |
|---|---:|
| Gate accuracy | 94.47% |
| Gate recall | 96.40% |
| Gate precision | 91.53% |
| Memory weighted recall | 60.97% |
| Memory weighted precision | 80.65% |
| Memory under-provisioning | 2.00% |
| Memory direct / safer reduction | 73.00% / 44.50% |
| Wall-time weighted recall | 84.15% |
| Wall-time weighted precision | 97.71% |
| Wall-time under-provisioning | 0.44% |
| Wall-time direct / safer reduction | 80.00% / 66.50% |

The quick validation can be repeated with:

```bash
bash sc26_artifact/run_quickcheck.sh
```

The complete model-based run is performed with:

```bash
bash sc26_artifact/run_ae.sh
```

That command obtains the released pretrained models, runs both held-out branches, checks the generated logs, and recreates the figures.
