#!/usr/bin/env python3
"""Preflight checks for the public rareHPC SC26 artifact."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = json.loads((Path(__file__).with_name("expected_results.json")).read_text())


def check(condition: bool, label: str, observed: object = None, expected: object = None) -> bool:
    status = "PASS" if condition else "FAIL"
    suffix = ""
    if observed is not None or expected is not None:
        suffix = f" (observed={observed!r}, expected={expected!r})"
    print(f"{status:4s} {label}{suffix}")
    return condition


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-models", action="store_true")
    args = parser.parse_args()

    required = [
        "README.md",
        "environment.yml",
        "requirements.txt",
        "download_models.py",
        "test.py",
        "train.py",
        "DataPreprocess.ipynb",
        "test.csv",
        "classification_model/encoders/ClassFier_bec_alldata.joblib",
        "MEMwithsampling/encoders/Regressor_bec_balanced_all_MEMwithsampling.joblib",
        "ComputeTimewithsampling/encoders/Regressor_bec_balanced_all_ComputeTimewithsampling.joblib",
        "paper_figures/generate_paper_figures.py",
        "paper_figures/data/figure_manifest.csv",
        "sc26_artifact/expected_results.json",
        "sc26_artifact/verify_outputs.py",
    ]
    ok = True
    for rel in required:
        ok &= check((ROOT / rel).is_file(), f"required file {rel}")

    env_text = (ROOT / "environment.yml").read_text(errors="replace")
    ok &= check("name: rareHPC" in env_text, "Conda environment is named rareHPC")

    df = pd.read_csv(ROOT / "test.csv")
    ref = EXPECTED["public_test_trace"]
    observations = {
        "rows": len(df),
        "encoded_users": int(df["id_user"].nunique()),
        "account_labels": int(df["account"].nunique()),
    }
    counts = df.groupby("id_user")["id_job"].transform("count")
    eligible = df[counts > 199]
    observations.update({
        "eligible_rows_after_history_filter": len(eligible),
        "eligible_users_after_history_filter": int(eligible["id_user"].nunique()),
        "eligible_accounts_after_history_filter": int(eligible["account"].nunique()),
    })
    for key, observed in observations.items():
        ok &= check(observed == ref[key], f"trace {key}", observed, ref[key])

    start = datetime.fromtimestamp(int(df["time_submit"].min()), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    end = datetime.fromtimestamp(int(df["time_submit"].max()), tz=timezone.utc).isoformat().replace("+00:00", "Z")
    ok &= check(start == ref["start_utc"], "trace start", start, ref["start_utc"])
    ok &= check(end == ref["end_utc"], "trace end", end, ref["end_utc"])

    model_paths = [
        ROOT / "classification_model/models/ClassFier_LGBM_alldata.joblib",
        ROOT / "MEMwithsampling/models/RandomForest_balanced_all_MEMwithsampling.joblib",
        ROOT / "ComputeTimewithsampling/models/RandomForest_balanced_all_ComputeTimewithsampling.joblib",
    ]
    models_ok = True
    for path in model_paths:
        present = path.is_file() and path.stat().st_size > 0
        print(f"{'PASS' if present else 'INFO':4s} model {path.relative_to(ROOT)} {'present' if present else 'not downloaded'}")
        models_ok &= present
    if args.require_models:
        ok &= check(models_ok, "all released model files are present")

    reference_figures = list((ROOT / "paper_figures/reference").glob("*.pdf"))
    ok &= check(len(reference_figures) == 8, "eight reference paper figures", len(reference_figures), 8)

    print("Preflight complete.")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
