#!/usr/bin/env python3
"""Parse public-pipeline logs and compare them with the released reference values."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = json.loads((Path(__file__).with_name("expected_results.json")).read_text())


def values(pattern: str, text: str) -> list[float]:
    return [float(x) for x in re.findall(pattern, text, flags=re.IGNORECASE)]


def close(label: str, observed: float, expected: float, tolerance: float) -> bool:
    passed = abs(observed - expected) <= tolerance
    print(
        f"{'PASS' if passed else 'FAIL':4s} {label}: "
        f"observed={observed:.2f}, expected={expected:.2f}, tolerance=+/-{tolerance:.2f}"
    )
    return passed


def parse_branch(path: Path, branch_key: str) -> bool:
    text = path.read_text(errors="replace")
    reference = EXPECTED["functional_pipeline"]
    ok = True

    recalls = values(r"Recall for Compute Utilization High/Low:\s*([0-9.]+)", text)
    precisions = values(r"Precision for Compute Utilization High/Low:\s*([0-9.]+)", text)
    accuracies = values(r"Accuracy for Compute Utilization High/Low:\s*([0-9.]+)", text)
    if not (recalls and precisions and accuracies):
        print(f"FAIL selective-gate metrics not found in {path}")
        return False

    gate = reference["classification"]
    ok &= close(f"{branch_key} gate accuracy", accuracies[-1], gate["accuracy_pct"], gate["tolerance_pct_points"])
    ok &= close(f"{branch_key} gate recall", recalls[-1], gate["recall_pct"], gate["tolerance_pct_points"])
    ok &= close(f"{branch_key} gate precision", precisions[-1], gate["precision_pct"], gate["tolerance_pct_points"])

    weighted_recall = values(r"weighted recall\s*([0-9.]+)", text)
    weighted_precision = values(r"weighted precision\s*([0-9.]+)", text)
    under = values(r"under-provisioning rate\s*([0-9.]+)", text)
    savings = values(r"([0-9.]+)\s*% average savings for", text)
    if not (weighted_recall and weighted_precision and under and len(savings) >= 2):
        print(f"FAIL branch metrics not found in {path}")
        return False

    ref = reference[branch_key]
    tol = ref["tolerance_pct_points"]
    ok &= close(f"{branch_key} weighted recall", weighted_recall[-1], ref["weighted_recall_pct"], tol)
    ok &= close(f"{branch_key} weighted precision", weighted_precision[-1], ref["weighted_precision_pct"], tol)
    ok &= close(f"{branch_key} under-provisioning", under[-1], ref["under_provisioning_pct"], tol)
    ok &= close(f"{branch_key} direct account-mean reduction", savings[-2], ref["direct_account_mean_reduction_pct"], tol)
    ok &= close(f"{branch_key} safer account-mean reduction", savings[-1], ref["safer_account_mean_reduction_pct"], tol)
    return ok


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--memory-log", type=Path, required=True)
    parser.add_argument("--walltime-log", type=Path, required=True)
    args = parser.parse_args()

    ok = parse_branch(args.memory_log, "memory")
    ok &= parse_branch(args.walltime_log, "wall_time")

    expected_files = [
        "classification_model/Classifier_cfm_test.png",
        "MEMwithsampling/cfm_MEMwithsampling_test.png",
        "MEMwithsampling/prf_MEMwithsampling_test.png",
        "MEMwithsampling/combined_savingsMEMwithsampling_test.png",
        "ComputeTimewithsampling/cfm_ComputeTimewithsampling_test.png",
        "ComputeTimewithsampling/prf_ComputeTimewithsampling_test.png",
        "ComputeTimewithsampling/combined_savingsComputeTimewithsampling_test.png",
    ]
    for rel in expected_files:
        path = ROOT / rel
        present = path.is_file() and path.stat().st_size > 0
        print(f"{'PASS' if present else 'FAIL':4s} output {rel}")
        ok &= present

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
