# Paper figure recreation

The directory `reference/` contains the eight final figure files used by the submitted manuscript. The script `generate_paper_figures.py` recreates those figures from the numerical inputs in `data/`.

```bash
python paper_figures/generate_paper_figures.py \
  --output-dir sc26_outputs/paper_figures
```

PDF, PNG, and SVG files are written to the selected output directory. Font rendering may vary slightly across Matplotlib installations, but the values, labels, panel organization, dimensions, and filenames are fixed by the distributed inputs.

## Provenance by figure

- Fig. 1 is generated from the workflow specification in the paper.
- Fig. 2 uses de-identified aggregate utilization values from the protected development trace.
- Fig. 3 combines frozen development-model summaries with the public held-out gate metrics.
- Figs. 4 and 6 use frozen validation operating-mode summaries.
- Fig. 5 uses the exact final-paper held-out summary values.
- Fig. 7 uses de-identified account-level summaries from the held-out week.
- Fig. 8 uses frozen memory and wall-time confusion matrices.

The raw 2.1-million-job development trace is not needed to redraw the figures. It is required only to recompute the protected development aggregates from individual production jobs. `data/figure_manifest.csv` records the input file and public-computation status for every figure.
