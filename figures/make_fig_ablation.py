#!/usr/bin/env python3
"""Regenerate figures/fig_ablation.pdf (R-matrix decomposition, 1x3 panels).

The previous export carried ~2,800pt of empty canvas below the three panels
(no ``bbox_inches="tight"``), which made the float ~2.8 pages tall and pushed
the surrounding tables around.  The values below are the ones printed on the
original figure (independent single-seed run; they differ slightly from the
R on/off table, as its caption states).

Usage:
    python make_fig_ablation.py [--out PATH]
"""

import argparse
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "serif"

GRAY = "#d9d9d9"
ORANGE = "#f4a582"
BLUE = "#0571b0"
GREEN = "#7fbf7b"
RED = "#d73027"

CONDITIONS = ["BCE\nonly", "Consistency\nloss", "Reconciliation\nonly", "Both\n(full R)"]
CONDITION_COLORS = [GRAY, ORANGE, BLUE, GREEN]

# (panel title, per-condition Micro-F1 — None when the arm was not run)
PANELS = [
    (
        "ArXiv\n(shallow tree, D=2)",
        [0.7288, 0.7202, 0.7303, 0.7291],
        (0.710, 0.740),
    ),
    (
        "cellcycle_FUN\n(deep tree, D=6)",
        [0.2734, 0.2698, 0.2734, 0.2762],
        (0.260, 0.290),
    ),
    (
        "cellcycle_GO\n(DAG, D=13, sparse)",
        [0.3955, None, 0.3953, None],
        (0.380, 0.410),
    ),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("fig_ablation.pdf"),
    )
    args = parser.parse_args()

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.0))
    positions = range(len(CONDITIONS))

    for ax, (title, values, ylim) in zip(axes, PANELS):
        heights = [value if value is not None else 0.0 for value in values]
        ax.bar(
            list(positions),
            heights,
            color=CONDITION_COLORS,
            edgecolor="black",
            linewidth=0.6,
            width=0.8,
            zorder=3,
        )
        for pos, value in zip(positions, values):
            if value is None:
                continue
            ax.text(
                pos,
                value + (ylim[1] - ylim[0]) * 0.012,
                f"{value:.4f}",
                ha="center",
                va="bottom",
                fontsize=7.5,
                fontweight="bold",
                zorder=4,
            )

        # Delta of reconciliation over plain BCE, labelled on the tallest of
        # the last two arms (matching the original figure's placement).
        baseline, reconciled = values[0], values[2]
        if baseline is not None and reconciled is not None:
            delta = reconciled - baseline
            anchor = max(
                (pos for pos in (2, 3) if values[pos] is not None),
                key=lambda pos: values[pos],
            )
            ax.text(
                anchor,
                values[anchor] + (ylim[1] - ylim[0]) * 0.075,
                f"$\\Delta$={delta:+.4f}",
                ha="center",
                va="bottom",
                fontsize=8,
                color=RED,
                zorder=4,
            )

        ax.set_xticks(list(positions))
        ax.set_xticklabels(CONDITIONS, fontsize=7.5)
        ax.set_ylim(*ylim)
        ax.set_ylabel("Micro-F1", fontsize=9)
        ax.set_title(title, fontsize=9)
        ax.grid(axis="y", color="#dddddd", linewidth=0.6, zorder=0)
        ax.set_axisbelow(True)

    fig.suptitle(
        "R-Matrix Decomposition: Where Does the Benefit Come From?",
        fontsize=12,
        fontweight="bold",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(args.out, bbox_inches="tight")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
