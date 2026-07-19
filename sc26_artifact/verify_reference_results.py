#!/usr/bin/env python3
"""Verify the numerical values encoded in the distributed held-out outputs.

This check is independent of model execution. It reconstructs the reported
classification and bucket metrics from CSV transcriptions of the confusion
matrices distributed with the public repository, and it verifies the account-
mean direct and safer reductions shown by the held-out operational plots.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REF = Path(__file__).with_name("reference_outputs")
EXPECTED = json.loads((Path(__file__).with_name("expected_results.json")).read_text())
ORDER = ["0-5", "6-10", "11-20", "21-50", ">50"]


def check_close(label: str, observed: float, expected: float, tolerance: float = 0.01) -> bool:
    ok = abs(observed - expected) <= tolerance
    print(
        f"{'PASS' if ok else 'FAIL':4s} {label}: "
        f"observed={observed:.2f}, expected={expected:.2f}, tolerance=+/-{tolerance:.2f}"
    )
    return ok


def matrix_from_long(path: Path, order: list[str]) -> np.ndarray:
    df = pd.read_csv(path)
    idx = {name: i for i, name in enumerate(order)}
    matrix = np.zeros((len(order), len(order)), dtype=int)
    for row in df.itertuples(index=False):
        matrix[idx[str(row.actual)], idx[str(row.predicted)]] = int(row.count)
    return matrix


def gate_metrics() -> dict[str, float]:
    c = matrix_from_long(REF / "heldout_gate_confusion.csv", ["Low", "High"])
    tn, fp = c[0, 0], c[0, 1]
    fn, tp = c[1, 0], c[1, 1]
    return {
        "accuracy_pct": 100.0 * (tp + tn) / c.sum(),
        "recall_pct": 100.0 * tp / (tp + fn),
        "precision_pct": 100.0 * tp / (tp + fp),
    }


def branch_metrics(path: Path) -> dict[str, float]:
    c = matrix_from_long(path, ORDER)
    support = c.sum(axis=1)
    recall = np.divide(np.diag(c), support, out=np.zeros(5, dtype=float), where=support > 0)
    predicted = c.sum(axis=0)
    precision = np.divide(np.diag(c), predicted, out=np.zeros(5, dtype=float), where=predicted > 0)
    total = c.sum()
    under = sum(c[i, j] for i in range(5) for j in range(i))
    return {
        "weighted_recall_pct": 100.0 * np.sum((support / total) * recall),
        "weighted_precision_pct": 100.0 * np.sum((support / total) * precision),
        "under_provisioning_pct": 100.0 * under / total,
    }


def reduction_metrics() -> dict[tuple[str, str], float]:
    df = pd.read_csv(REF / "heldout_account_reductions.csv")
    return {
        (str(resource), str(mode)): float(group["reduction_pct"].mean())
        for (resource, mode), group in df.groupby(["resource", "mode"], sort=False)
    }


def main() -> int:
    ok = True
    functional = EXPECTED["functional_pipeline"]

    gate = gate_metrics()
    for key, value in gate.items():
        ok &= check_close(f"selective gate {key}", value, functional["classification"][key])

    reductions = reduction_metrics()
    for branch, filename, resource in [
        ("memory", "heldout_memory_confusion.csv", "memory"),
        ("wall_time", "heldout_walltime_confusion.csv", "wall_time"),
    ]:
        observed = branch_metrics(REF / filename)
        expected = functional[branch]
        for key, value in observed.items():
            ok &= check_close(f"{branch} {key}", value, expected[key])
        ok &= check_close(
            f"{branch} direct account-mean reduction",
            reductions[(resource, "direct")],
            expected["direct_account_mean_reduction_pct"],
        )
        ok &= check_close(
            f"{branch} safer account-mean reduction",
            reductions[(resource, "safer")],
            expected["safer_account_mean_reduction_pct"],
        )

    print("Reference-output verification complete.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
