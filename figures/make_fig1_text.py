#!/usr/bin/env python3
"""Regenerate figures/fig1_sota_comparison.pdf (text benchmarks against published results).

Published values are those of Table ``tab:text``.  Ours: frozen SPECTER2 + R (ArXiv, mean
of three seeds) and fine-tuned SPECTER2 + R on WOS under HPT's protocol
(``hmc-torch/experiments/run_wos_e2e.py --epochs 10``, seed 0, 2026-10-20).  Only WOS is a
like-for-like comparison; the ArXiv baselines use other label sets and splits.

Usage:
    python make_fig1_text.py [--out PATH]
"""

import argparse
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["font.family"] = "serif"

PUBLISHED = "#95a5a6"
OURS = "#1a5276"

# (method, value, ours?) per panel, in plotting order.
PANELS = {
    "ArXiv (156 classes, not like-for-like)": [
        ("HiAGM", 0.5950, False),
        ("HTC-infoMAX", 0.6130, False),
        ("Ours (frozen)", 0.7295, True),
    ],
    "WOS (142 classes)": [
        ("HiAGM", 0.8604, False),
        ("HTC-infoMAX", 0.8630, False),
        ("HGCLR", 0.8711, False),
        ("HPT", 0.8716, False),
        ("Ours (fine-tuned)", 0.8671, True),
    ],
}
LIMITS = {"ArXiv (156 classes, not like-for-like)": (0.55, 0.78),
          "WOS (142 classes)": (0.85, 0.88)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path,
                        default=Path(__file__).with_name("fig1_sota_comparison.pdf"))
    args = parser.parse_args()

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8))
    for ax, (title, rows) in zip(axes, PANELS.items()):
        names = [name for name, _, _ in rows]
        values = [value for _, value, _ in rows]
        colors = [OURS if ours else PUBLISHED for _, _, ours in rows]
        ax.bar(range(len(rows)), values, color=colors, width=0.7)
        low, high = LIMITS[title]
        for pos, value in enumerate(values):
            ax.text(pos, value + (high - low) * 0.01, f"{value:.4f}", ha="center", fontsize=8)
        ax.set_ylim(low, high)
        ax.set_xticks(range(len(rows)))
        ax.set_xticklabels(names, rotation=20, ha="right", fontsize=8)
        ax.set_ylabel("Micro-F1", fontsize=9)
        ax.set_title(title, fontsize=10)
    fig.suptitle("Text HMC Benchmarks: Ours against Published Results",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(args.out, bbox_inches="tight")
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()
