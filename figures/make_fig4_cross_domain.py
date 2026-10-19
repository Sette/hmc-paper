#!/usr/bin/env python3
"""Regenerate figures/fig4_cross_domain.pdf (cross-domain Micro-F1 overview).

The ARFF bars (FunCat, GO, cross-domain) are the BCE-trained MLP with
reconciliation under the validation-only protocol, mean of three seeds, from
``hmc-torch/experiments/run_protocol.py`` (``output/protocol/*.json``; GO from
``output/protocol_go_recipe/bce/``).  The text bars repeat values already
reported in the paper's tables.  ``--results`` still accepts a
``run_cross_domain.py`` JSON to override the cross-domain bars.

Usage:
    python make_fig4_cross_domain.py [--results PATH] [--out PATH]
"""

import argparse
import json
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "serif"

COLORS = {
    "Scientific Text": "#1a5276",
    "Email": "#27ae60",
    "Medical Images": "#e74c3c",
    "Microscopy": "#8e44ad",
    "Genomics": "#f39c12",
}

# (label, second line, legend group, micro-F1) in plotting order, bottom first.
# ARFF values: run_protocol.py, BCE + reconciliation, mean of seeds 0/42/123
# (2026-10-19); text values from the paper's tables.
SERIES = [
    ("ArXiv", "", "Scientific Text", 0.730),
    ("WOS", "", "Scientific Text", 0.874),
    ("enron", "", "Email", 0.674),
    ("imclef07a", "", "Medical Images", 0.899),
    ("imclef07d", "", "Medical Images", 0.848),
    ("diatoms", "", "Microscopy", 0.752),
    ("cellcycle", "FUN", "Genomics", 0.301),
    ("seq", "FUN", "Genomics", 0.325),
    ("expr", "GO", "Genomics", 0.454),
    ("seq", "GO", "Genomics", 0.461),
]

# Dataset keys in global_results.json for the cross-domain bars.
RESULTS_KEYS = {
    "enron": "enron_others",
    "diatoms": "diatoms_others",
    "imclef07a": "imclef07a_others",
    "imclef07d": "imclef07d_others",
}


def load_results(path):
    """Return ``{dataset: micro_f1}`` from a run_cross_domain.py JSON file."""
    with open(path, encoding="utf-8") as handle:
        return {name: row["micro_f1"] for name, row in json.load(handle).items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results",
        type=Path,
        default=None,
        help="global_results.json produced by run_cross_domain.py (optional)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).with_name("fig4_cross_domain.pdf"),
    )
    args = parser.parse_args()

    series = list(SERIES)
    if args.results:
        measured = load_results(args.results)
        series = [
            (name, second, group, measured.get(RESULTS_KEYS.get(name), value))
            for name, second, group, value in series
        ]

    labels = [f"{name}\n{second}" if second else name for name, second, _, _ in series]
    groups = [group for _, _, group, _ in series]
    values = [value for _, _, _, value in series]

    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    positions = list(range(len(values)))
    ax.barh(positions, values, color=[COLORS[group] for group in groups], height=0.75)

    for pos, value in zip(positions, values):
        ax.text(value + 0.005, pos, f"{value:.3f}", va="center", fontsize=9)

    ax.set_yticks(positions)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Micro-F1", fontsize=10)
    ax.set_title(
        "HMC-Torch: Cross-Domain Performance (Global MLP + R-Matrix)",
        fontsize=12,
        fontweight="bold",
    )

    legend_groups = list(dict.fromkeys(groups))
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=COLORS[group]) for group in legend_groups
    ]
    ax.legend(handles, legend_groups, loc="lower right", fontsize=8, framealpha=0.95)

    fig.savefig(args.out, bbox_inches="tight")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
