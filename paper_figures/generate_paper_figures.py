#!/usr/bin/env python3
"""Regenerate the eight figures used in the RARE-HPC paper.

The script reads only the frozen, de-identified summary files distributed in
``paper_figures/data``.  It does not require the protected development trace.
The original figure files from the submitted LaTeX package are retained under
``paper_figures/reference`` and are not overwritten.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

BLUE = "#2C6AA0"
ORANGE = "#E69F00"
SKY = "#56B4E9"
GREEN = "#009E73"
LIGHT_GREEN = "#8CCB7E"
ROSE = "#CC6677"
GRID = "#D8DEE9"
DARK = "#182234"
PALE_BLUE = "#EAF2F8"
PALE_ORANGE = "#FFF2D5"
PALE_GREEN = "#E9F5EF"
PALE_GRAY = "#F3F4F6"
BORDER_GRAY = "#6B7280"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.titlesize": 9,
    "axes.titleweight": "bold",
    "axes.labelsize": 8,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": GRID,
    "grid.linewidth": 0.55,
    "grid.alpha": 0.9,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
})


def save_all(fig: plt.Figure, outdir: Path, stem: str) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(outdir / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(outdir / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(outdir / f"{stem}.svg", bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, title, body, edge=BLUE, face=PALE_BLUE,
        title_size=9, body_size=7.5, radius=0.018):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.008,rounding_size={radius}",
        linewidth=1.7, edgecolor=edge, facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h * 0.63, title, ha="center", va="center",
            fontsize=title_size, fontweight="bold", color=DARK, linespacing=0.92)
    if body:
        ax.text(x + w / 2, y + h * 0.30, body, ha="center", va="center",
                fontsize=body_size, color=DARK, linespacing=0.92)
    return patch


def arrow(ax, start, end, color=DARK, dashed=False, lw=1.4, mutation=9):
    style = "--" if dashed else "-"
    a = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=mutation,
                        linewidth=lw, linestyle=style, color=color,
                        shrinkA=0, shrinkB=0, connectionstyle="arc3")
    ax.add_patch(a)
    return a


def fig1_workflow(outdir: Path) -> None:
    """Recreate the final workflow diagram used as Fig. 1.

    Coordinates, labels, line styles, and output dimensions follow the final
    vector figure distributed in ``paper_figures/reference``.  The diagram is
    generated from primitives so it remains editable in SVG/PDF form.
    """
    fig, ax = plt.subplots(figsize=(7.28, 3.88))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Main recommendation path.
    box(ax, 0.015, 0.765, 0.120, 0.125, "Request",
        "mem/time\nCPU/GPU, name", title_size=8.4, body_size=6.6,
        radius=0.012)
    box(ax, 0.155, 0.765, 0.155, 0.125, "Features",
        "request fields\n+ history", title_size=8.4, body_size=6.6,
        radius=0.012)

    cx, cy, dw, dh = 0.372, 0.827, 0.104, 0.142
    diamond = Polygon([
        (cx, cy + dh / 2), (cx + dw / 2, cy),
        (cx, cy - dh / 2), (cx - dw / 2, cy)
    ], closed=True, edgecolor=BLUE, facecolor=PALE_BLUE, linewidth=1.7)
    ax.add_patch(diamond)
    ax.text(cx, cy, "Selective\ngate", ha="center", va="center",
            fontsize=7.9, fontweight="bold", color=DARK, linespacing=0.93)
    ax.text(cx + 0.010, cy - dh / 2 - 0.018, "Optimize?", ha="left",
            va="top", fontsize=6.1, fontweight="bold", color=DARK)

    box(ax, 0.442, 0.765, 0.135, 0.125, "Predict",
        "memory %\nwall-time %", title_size=8.4, body_size=6.6,
        radius=0.012)
    box(ax, 0.597, 0.765, 0.170, 0.125, "Policy layer",
        "buckets + mode\ndirect or safer", edge=ORANGE,
        face=PALE_ORANGE, title_size=8.4, body_size=6.5, radius=0.012)

    box(ax, 0.344, 0.475, 0.145, 0.115, "Pass-through",
        "original request", edge=BORDER_GRAY, face=PALE_GRAY,
        title_size=7.8, body_size=6.2, radius=0.010)
    box(ax, 0.610, 0.415, 0.160, 0.115, "User review",
        "accept / edit / reject", edge=ORANGE, face=PALE_ORANGE,
        title_size=7.8, body_size=6.2, radius=0.010)
    box(ax, 0.835, 0.415, 0.110, 0.115, "SLURM", "schedule",
        edge=GREEN, face=PALE_GREEN, title_size=7.8, body_size=6.2,
        radius=0.010)
    box(ax, 0.155, 0.145, 0.155, 0.115, "History store",
        "executed jobs\nusage logs", edge=GREEN, face=PALE_GREEN,
        title_size=7.7, body_size=6.1, radius=0.010)

    # Solid recommendation path.
    arrow(ax, (0.135, 0.827), (0.155, 0.827), lw=1.45, mutation=8)
    arrow(ax, (0.310, 0.827), (cx - dw / 2, 0.827), lw=1.45, mutation=8)
    arrow(ax, (cx + dw / 2, 0.827), (0.442, 0.827), lw=1.45, mutation=8)
    arrow(ax, (0.577, 0.827), (0.597, 0.827), lw=1.45, mutation=8)
    arrow(ax, (0.682, 0.765), (0.682, 0.530), color=ORANGE,
          lw=1.45, mutation=8)
    arrow(ax, (0.770, 0.472), (0.835, 0.472), color=GREEN,
          lw=1.45, mutation=8)

    # Dashed pass-through route.
    arrow(ax, (cx, cy - dh / 2), (cx, 0.590), color=BORDER_GRAY,
          dashed=True, lw=1.25, mutation=7)
    ax.text(0.425, 0.625, "low expected\nbenefit", ha="left", va="center",
            fontsize=6.1, color=BORDER_GRAY, fontweight="bold",
            linespacing=0.90)
    ax.plot([0.489, 0.535, 0.535, 0.835], [0.532, 0.532, 0.357, 0.357],
            linestyle="--", color=BORDER_GRAY, linewidth=1.25)
    arrow(ax, (0.835, 0.357), (0.867, 0.415), color=BORDER_GRAY,
          dashed=True, lw=1.25, mutation=7)
    ax.text(0.690, 0.387, "unchanged request to scheduler", ha="center",
            va="bottom", fontsize=5.8, color=BORDER_GRAY,
            fontweight="bold")

    # Green execution-feedback loop and historical context.
    ax.plot([0.892, 0.892, 0.310], [0.415, 0.218, 0.218],
            color=GREEN, linewidth=1.35)
    arrow(ax, (0.310, 0.218), (0.310, 0.218), color=GREEN,
          lw=1.35, mutation=7)
    arrow(ax, (0.892, 0.218), (0.310, 0.218), color=GREEN,
          lw=1.35, mutation=7)
    arrow(ax, (0.232, 0.260), (0.232, 0.765), color=GREEN,
          lw=1.35, mutation=7)
    ax.text(0.585, 0.246, "execution feedback updates future features",
            ha="center", va="bottom", fontsize=6.2, color=GREEN,
            fontweight="bold")
    ax.text(0.249, 0.510, "historical context", rotation=90,
            ha="center", va="center", fontsize=6.0, color=GREEN,
            fontweight="bold")

    # Line-style legend.
    yleg = 0.035
    ax.plot([0.025, 0.055], [yleg, yleg], color=DARK, linewidth=1.35)
    ax.text(0.060, yleg, "recommendation path", va="center",
            fontsize=5.5, color=BORDER_GRAY)
    ax.plot([0.235, 0.265], [yleg, yleg], color=BORDER_GRAY,
            linewidth=1.35, linestyle="--")
    ax.text(0.270, yleg, "pass-through path", va="center",
            fontsize=5.5, color=BORDER_GRAY)
    ax.plot([0.445, 0.475], [yleg, yleg], color=GREEN, linewidth=1.35)
    ax.text(0.480, yleg, "feedback loop", va="center",
            fontsize=5.5, color=BORDER_GRAY)

    save_all(fig, outdir, "fig1_workflow")


def fig2_utilization(outdir: Path) -> None:
    df = pd.read_csv(DATA / "fig2_jubail_utilization.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.19, 3.39))
    configs = [
        ("memory", "Memory request utilization", "Used / requested memory (%)"),
        ("walltime", "Wall-time request utilization", "Used / requested wall time (%)"),
    ]
    for ax, (panel, title, xlabel) in zip(axes, configs):
        d = df[df.panel == panel].sort_values("order", ascending=False)
        y = np.arange(len(d))
        h = 0.35
        ax.barh(y + h/2, d["mean"], h, color=SKY, label="Mean")
        ax.barh(y - h/2, d["median"], h, color=ORANGE, label="Median")
        short = {
            "psychology": "psych.", "nyushanghai": "nyu-sh",
            "ecomputer": "ecomp", "scomputer": "scomp",
            "collaborator": "collab", "mathematics": "math",
            "socialscience": "soc.sci", "mechanical": "mech",
            "electrical": "elect"
        }
        labels = [short.get(v, v) for v in d.account]
        ax.set_yticks(y, labels)
        ax.set_xlabel(xlabel)
        ax.set_title(title)
        ax.grid(axis="x")
        ax.grid(axis="y", visible=False)
        xmax = max(d["mean"].max(), d["median"].max()) * 1.16
        ax.set_xlim(0, xmax)
        for yy, val in zip(y + h/2, d["mean"]):
            ax.text(val + xmax*0.012, yy, f"{val:g}", va="center", fontsize=6.2)
        for yy, val in zip(y - h/2, d["median"]):
            ax.text(val + xmax*0.012, yy, f"{val:g}", va="center", fontsize=6.2)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=False,
               bbox_to_anchor=(0.5, 1.01))
    fig.subplots_adjust(wspace=0.25, top=0.82, bottom=0.13, left=0.09, right=0.99)
    save_all(fig, outdir, "fig2_jubail_utilization_nature")


def label_bars(ax, bars, fmt="{:.2f}", fontsize=6.5):
    for bar in bars:
        value = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, value, fmt.format(value),
                ha="center", va="bottom", fontsize=fontsize)


def fig3_models_gate(outdir: Path) -> None:
    mae = pd.read_csv(DATA / "fig3_model_mae.csv")
    gate = pd.read_csv(DATA / "verified_classification_metrics.csv")
    fig, axes = plt.subplots(1, 3, figsize=(7.18, 2.21))

    colors = [GREEN, LIGHT_GREEN, LIGHT_GREEN, ROSE]
    b1 = axes[0].bar(mae.Model, mae.Memory, color=colors, width=0.65)
    axes[0].set_title("Memory MAE")
    axes[0].set_ylabel("MAE (pp)")
    axes[0].set_ylim(0, 4.0)
    label_bars(axes[0], b1)

    b2 = axes[1].bar(mae.Model, mae["Wall time"], color=colors, width=0.65)
    axes[1].set_title("Wall-time MAE")
    axes[1].set_ylim(0, 11.1)
    label_bars(axes[1], b2)

    metrics = ["Accuracy", "Recall", "Precision"]
    x = np.arange(3)
    width = 0.35
    val = [float(gate[(gate.Split == "Validation") & (gate.Metric == m)].Value.iloc[0]) for m in metrics]
    hold = [float(gate[(gate.Split == "Pipeline") & (gate.Metric == m)].Value.iloc[0]) for m in metrics]
    bars_v = axes[2].bar(x - width/2, val, width, color=BLUE, label="Validation")
    bars_h = axes[2].bar(x + width/2, hold, width, color=ORANGE, label="Held-out")
    axes[2].set_xticks(x, ["Acc.", "Recall", "Prec."])
    axes[2].set_ylim(88, 100)
    axes[2].set_ylabel("Score (%)")
    axes[2].set_title("Selective gate")
    handles, labels = axes[2].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.83, 1.01))
    fig.subplots_adjust(wspace=0.34, top=0.78, left=0.07, right=0.99, bottom=0.16)
    save_all(fig, outdir, "fig3_models_gate_nature")


def fig4_operating(outdir: Path) -> None:
    df = pd.read_csv(DATA / "verified_operating_modes.csv")
    resources = ["Memory", "Compute time"]
    labels = ["Memory", "Wall time"]
    fig, axes = plt.subplots(1, 2, figsize=(7.18, 2.60))
    x = np.arange(2)
    width = 0.36
    for ax, metric, title, ylabel in [
        (axes[0], "Reduction", "Recovery", "Over-request reduction (%)"),
        (axes[1], "UnderProv", "Safety risk", "Under-provisioning (%)"),
    ]:
        direct = [float(df[(df.Resource == r) & (df.Config == "Config 1")][metric].iloc[0]) for r in resources]
        safer = [float(df[(df.Resource == r) & (df.Config == "Config 2")][metric].iloc[0]) for r in resources]
        b1 = ax.bar(x - width/2, direct, width, color=BLUE, label="Direct")
        b2 = ax.bar(x + width/2, safer, width, color=ORANGE, label="Safer")
        ax.set_xticks(x, labels)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        label_bars(ax, b1)
        label_bars(ax, b2)
    axes[0].legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(1.05, 1.25))
    axes[0].set_ylim(0, 85)
    axes[1].set_ylim(0, 2.75)
    fig.subplots_adjust(wspace=0.34, top=0.78, left=0.07, right=0.99, bottom=0.17)
    save_all(fig, outdir, "fig4_operating_modes_nature")


def fig5_pipeline(outdir: Path) -> None:
    df = pd.read_csv(DATA / "verified_pipeline_metrics.csv")
    metrics = ["Weighted recall", "Weighted precision", "Under-provisioning", "Reduction Config 1", "Reduction Config 2"]
    labels = ["W.\nrecall", "W.\nprecision", "Under-\nprov.", "Direct\nred.", "Safer\nred."]
    x = np.arange(len(metrics))
    width = 0.34
    memory = [float(df[(df.Branch == "Memory") & (df.Metric == m)].Value.iloc[0]) for m in metrics]
    wall = [float(df[(df.Branch == "Compute time") & (df.Metric == m)].Value.iloc[0]) for m in metrics]
    fig, ax = plt.subplots(figsize=(3.43, 2.27))
    b1 = ax.bar(x - width/2, memory, width, color=SKY, label="Memory")
    b2 = ax.bar(x + width/2, wall, width, color=GREEN, label="Wall time")
    ax.set_xticks(x, labels)
    ax.set_ylabel("Value (%)")
    ax.set_ylim(0, 108)
    ax.legend(frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.5, 1.12))
    label_bars(ax, b1, fontsize=5.9)
    label_bars(ax, b2, fontsize=5.9)
    fig.subplots_adjust(top=0.82, left=0.15, right=0.98, bottom=0.20)
    save_all(fig, outdir, "fig5_pipeline_summary_column")


def fig6_frontier(outdir: Path) -> None:
    df = pd.read_csv(DATA / "verified_operating_modes.csv")
    fig, ax = plt.subplots(figsize=(3.52, 2.60))
    points = [
        ("Memory", "Config 1", BLUE, "Mem direct", (4, 3)),
        ("Memory", "Config 2", ORANGE, "Mem safer", (4, 3)),
        ("Compute time", "Config 1", GREEN, "Wall direct", (4, 3)),
        ("Compute time", "Config 2", ROSE, "Wall safer", (4, -9)),
    ]
    for resource, config, color, label, offset in points:
        r = df[(df.Resource == resource) & (df.Config == config)].iloc[0]
        ax.scatter(r.UnderProv, r.Reduction, s=42, color=color, zorder=3)
        ax.annotate(label, (r.UnderProv, r.Reduction), xytext=offset,
                    textcoords="offset points", fontsize=6.4)
    ax.set_xlabel("Under-provisioning (%)")
    ax.set_ylabel("Over-request reduction (%)")
    ax.set_title("Safety-efficiency frontier")
    ax.set_xlim(0, 2.8)
    ax.set_ylim(59, 78.5)
    fig.subplots_adjust(top=0.84, left=0.17, right=0.96, bottom=0.20)
    save_all(fig, outdir, "fig6_frontier_nature")


def fig7_accounts(outdir: Path) -> None:
    df = pd.read_csv(DATA / "fig7_account_holdout.csv")
    fig, axes = plt.subplots(2, 1, figsize=(3.43, 3.01), sharex=True)
    x = np.arange(4)
    width = 0.34
    for ax, resource in zip(axes, ["Memory", "Wall time"]):
        d = df[df.Resource == resource]
        b1 = ax.bar(x - width/2, d.Direct, width, color=BLUE, label="Direct")
        b2 = ax.bar(x + width/2, d.Safer, width, color=ORANGE, label="Safer")
        ax.set_ylabel("Reduction (%)")
        ax.set_title(resource)
        ax.set_ylim(0, 105)
        label_bars(ax, b1, fmt="{:.0f}%", fontsize=5.8)
        label_bars(ax, b2, fmt="{:.0f}%", fontsize=5.8)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, ncol=2, loc="upper center", bbox_to_anchor=(0.73, 0.995))
    axes[1].set_xticks(x, ["A1", "A2", "A3", "A4"])
    fig.subplots_adjust(hspace=0.47, top=0.88, left=0.15, right=0.98, bottom=0.12)
    save_all(fig, outdir, "fig7_account_holdout_column")


def compact_number(v: int) -> str:
    if abs(v) >= 1000:
        return f"{v/1000:.1f}k"
    return str(int(v))


def heatmap_panel(ax, matrix: np.ndarray, title: str) -> None:
    im = ax.imshow(matrix, cmap="Blues", aspect="equal")
    labels = ["0-5", "6-10", "11-20", "21-50", ">50"]
    ax.set_xticks(np.arange(5), labels)
    ax.set_yticks(np.arange(5), labels)
    ax.set_xlabel("Ground truth bucket")
    ax.set_ylabel("Predicted bucket")
    ax.set_title(title)
    threshold = matrix.max() * 0.52
    for i in range(5):
        for j in range(5):
            ax.text(j, i, compact_number(int(matrix[i, j])), ha="center", va="center",
                    fontsize=5.7, color="white" if matrix[i, j] > threshold else DARK)
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)


def fig8_confusion(outdir: Path) -> None:
    mem = pd.read_csv(DATA / "fig8_memory_confusion.csv", index_col=0).to_numpy()
    wall = pd.read_csv(DATA / "fig8_walltime_confusion.csv", index_col=0).to_numpy()
    fig, axes = plt.subplots(1, 2, figsize=(7.18, 2.75))
    heatmap_panel(axes[0], mem, "Memory buckets")
    heatmap_panel(axes[1], wall, "Wall-time buckets")
    fig.suptitle("Bucketed prediction errors after imbalance correction", y=0.99, fontsize=9)
    fig.subplots_adjust(wspace=0.28, top=0.82, left=0.08, right=0.98, bottom=0.16)
    save_all(fig, outdir, "fig8_confusion_compact_nature")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "generated")
    parser.add_argument("--figures", nargs="*", type=int, choices=range(1, 9),
                        default=list(range(1, 9)))
    args = parser.parse_args()
    functions = {
        1: fig1_workflow,
        2: fig2_utilization,
        3: fig3_models_gate,
        4: fig4_operating,
        5: fig5_pipeline,
        6: fig6_frontier,
        7: fig7_accounts,
        8: fig8_confusion,
    }
    for number in args.figures:
        functions[number](args.output_dir)
    print(f"Generated {len(args.figures)} figure(s) in {args.output_dir}")


if __name__ == "__main__":
    main()
