#!/usr/bin/env python3
"""Optional publication-style rendering of verified tables; requires matplotlib.

Does not recompute or modify the reference statistics. No model or network calls.
Usage: python3 plot_genomes.py --input ../reference-output --out NEW_DIRECTORY
"""
import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

INK = "#182D3A"
MUTED = "#5C6F7A"
TEAL = "#007E87"
ORANGE = "#CF602D"
PURPLE = "#71549B"
GRID = "#E1E7E9"
PAPER = "#FBFCFC"
LABELS = {"archaea": "Archaea", "bacteria": "Bacteria", "protozoa": "Protozoa",
          "fungi": "Fungi", "invertebrate": "Invertebrates", "plant": "Plants",
          "vertebrate_other": "Other vertebrates", "vertebrate_mammalian": "Mammals"}


def read_rows(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def configure():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
        "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED,
        "ytick.color": INK, "axes.edgecolor": GRID, "axes.facecolor": PAPER,
        "figure.facecolor": PAPER, "svg.fonttype": "none", "svg.hashsalt": "genome-demo",
        "savefig.facecolor": PAPER, "axes.titleweight": "bold"})


def heading(fig, index, title, subtitle):
    fig.text(.055, .952, f"GENOME ATLAS   /   {index}   /   NCBI REFERENCE ASSEMBLIES",
             fontsize=10, color=TEAL, weight="bold")
    fig.text(.055, .893, title, fontsize=27, weight="bold")
    fig.text(.055, .849, subtitle, fontsize=12.5, color=MUTED)


def base_axis(ax, n):
    ax.set_ylim(n - .5, -.5)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", length=0, pad=10)
    ax.set_yticks(range(n), labels=[])
    ax.grid(axis="x", color=GRID, linewidth=.8)


def sample_column(fig, box, rows):
    ax = fig.add_axes(box)
    ax.set_xlim(0, 1)
    ax.set_ylim(len(rows) - .5, -.5)
    ax.axis("off")
    ax.text(.99, 1.10, "ASSEMBLIES", transform=ax.transAxes, ha="right",
            fontsize=11, weight="bold")
    ax.text(.44, 1.025, "All", transform=ax.transAxes, ha="right", color=TEAL, fontsize=10)
    ax.text(.99, 1.025, "Complete", transform=ax.transAxes, ha="right", color=ORANGE, fontsize=10)
    for y, row in enumerate(rows):
        ax.text(.44, y, f'{int(row["all_n"]):,}', ha="right", va="center", fontsize=11)
        small = int(row["complete_n"]) < 10
        ax.text(.99, y, f'{int(row["complete_n"]):,}' + (" *" if small else ""),
                ha="right", va="center", fontsize=11, color=ORANGE if small else INK,
                weight="bold" if small else "normal")


def footer(fig, first, second):
    fig.add_artist(Line2D([.055, .947], [.12, .12], transform=fig.transFigure, color=GRID))
    fig.text(.055, .088, first, fontsize=10.5, color=INK)
    fig.text(.055, .057, second, fontsize=10, color=MUTED)
    fig.text(.055, .029, "Source: supplied NCBI RefSeq snapshot · 18 Sep 2026 · Unit of observation: assembly, not species.",
             fontsize=9, color=MUTED)


def save(fig, out, name):
    fig.savefig(out / f"{name}.png", dpi=160)
    fig.savefig(out / f"{name}.svg", metadata={"Date": None})
    plt.close(fig)


def overview(rows, out):
    fig = plt.figure(figsize=(16, 9.6))
    heading(fig, "01", "Larger genomes, fewer genes per megabase",
            "Group medians across all reference assemblies and the complete-genome subset. Both axes are logarithmic.")
    fig.legend(handles=[Line2D([], [], color=TEAL, marker="o", linestyle="none", markersize=8, label="All reference assemblies"),
                        Line2D([], [], color=ORANGE, marker="D", linestyle="none", markersize=7, label="Complete genomes only")],
               loc="upper left", bbox_to_anchor=(.05, .815), ncol=2, frameon=False, fontsize=11)
    specs = [([.21, .225, .275, .49], "GENOME SIZE", "Megabases (Mb)", "all_size_mb", "complete_size_mb", [1, 10, 100, 1000], (.8, 5500)),
             ([.53, .225, .275, .49], "GENE DENSITY", "Annotated genes per Mb", "all_density", "complete_density", [10, 100, 1000], (8, 1700))]
    for i, (box, title, unit, akey, ckey, ticks, bounds) in enumerate(specs):
        ax = fig.add_axes(box)
        base_axis(ax, len(rows))
        ax.set_xscale("log")
        ax.set_xlim(*bounds)
        ax.xaxis.set_major_locator(FixedLocator(ticks))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:,.0f}"))
        ax.xaxis.set_minor_locator(NullLocator())
        ax.set_xlabel(unit + " · log scale", fontsize=11, labelpad=14)
        ax.set_title(title, fontsize=11, loc="left", pad=38)
        if i == 0:
            ax.set_yticklabels([LABELS[r["group"]] for r in rows], fontsize=12)
        for y, row in enumerate(rows):
            a, c = float(row[akey]), float(row[ckey])
            ax.plot([a, c], [y - .085, y + .085], color="#A8B6BF", linewidth=1.7, zorder=2)
            ax.scatter(a, y - .085, color=TEAL, s=68, zorder=3, edgecolor=PAPER, linewidth=.8)
            ax.scatter(c, y + .085, color=ORANGE, marker="D", s=55, zorder=3, edgecolor=PAPER, linewidth=.8)
    sample_column(fig, [.835, .225, .112, .49], rows)
    footer(fig, "25,965 assemblies overall → 7,268 complete genomes.  * Complete subset contains fewer than 10 assemblies.",
           "Density is calculated per assembly, then summarized by its median. Categories are ordered by median genome size (all assemblies).")
    save(fig, out, "genome-overview")


def shifts(rows, out):
    fig = plt.figure(figsize=(16, 9.6))
    heading(fig, "02", "Filtering changes the sample—and the story",
            "Change in each group median after retaining only complete genomes, relative to all reference assemblies.")
    fig.legend(handles=[Patch(facecolor=TEAL, label="Genome size"), Patch(facecolor=PURPLE, label="Gene density"),
                        Patch(facecolor=PAPER, edgecolor=MUTED, hatch="////", label="Complete subset n < 10")],
               loc="upper left", bbox_to_anchor=(.05, .815), ncol=3, frameon=False, fontsize=11)
    for i, (box, key, title, colour) in enumerate([
            ([.21, .225, .275, .49], "size_change_pct", "GENOME SIZE", TEAL),
            ([.53, .225, .275, .49], "density_change_pct", "GENE DENSITY", PURPLE)]):
        ax = fig.add_axes(box)
        base_axis(ax, len(rows))
        ax.set_xlim(-75, 105)
        ax.set_xticks([-50, 0, 50, 100], ["−50%", "0", "+50%", "+100%"])
        ax.axvline(0, color=MUTED, linewidth=1.1)
        ax.set_xlabel("Change in median (%)", fontsize=11, labelpad=14)
        ax.set_title(title, fontsize=11, loc="left", pad=38)
        if i == 0:
            ax.set_yticklabels([LABELS[r["group"]] for r in rows], fontsize=12)
        for y, row in enumerate(rows):
            value = float(row[key])
            small = int(row["complete_n"]) < 10
            ax.barh(y, value, height=.44, color=colour, edgecolor=PAPER,
                    linewidth=.4, hatch="////" if small else None, zorder=3)
            text = "≈0%" if abs(value) < .05 else f"{value:+.1f}%".replace("-", "−")
            ax.text(value + (2.2 if value >= 0 else -2.2), y, text,
                    ha="left" if value >= 0 else "right", va="center", fontsize=10.5, color=INK)
    sample_column(fig, [.835, .225, .112, .49], rows)
    footer(fig, "The +79.0% gene-density shift in other vertebrates is based on just 3 complete assemblies, versus 622 overall.",
           "Hatching is a descriptive small-sample flag, not a significance test. These nested, selected cohorts do not isolate assembly-quality effects.")
    save(fig, out, "complete-assembly-shift")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="Directory containing verified summary.csv and comparison.csv")
    parser.add_argument("--out", type=Path, required=True, help="New output directory; never overwrite")
    args = parser.parse_args()
    rows = read_rows(args.input / "comparison.csv")
    if len(rows) != 8 or {r["group"] for r in rows} != set(LABELS):
        raise ValueError("This designed reference layout expects exactly the eight supplied NCBI groups")
    rows.sort(key=lambda r: float(r["all_size_mb"]))
    # Fixed captions belong to this verified reference, not arbitrary new data.
    if sum(int(r["all_n"]) for r in rows) != 25965 or sum(int(r["complete_n"]) for r in rows) != 7268:
        raise ValueError("Reference counts differ; update the layout and captions for a different dataset")
    summary = read_rows(args.input / "summary.csv")
    for r in summary:
        if r["valid_size_n"] != r["assemblies"] or r["valid_density_n"] != r["assemblies"]:
            raise ValueError("Missing values require separate metric denominators in the figure")
    args.out.mkdir(parents=True, exist_ok=False)
    configure()
    overview(rows, args.out)
    shifts(rows, args.out)
    svgs = [(args.out / f"{name}.svg").read_text() for name in ("genome-overview", "complete-assembly-shift")]
    # Inline SVG keeps the browser version self-contained and zoomable.
    panels = "\n".join("<section>" + s[s.index("<svg"):].replace("<svg ", '<svg role="img" aria-label="' + label + '" ', 1) + "</section>"
                       for s, label in zip(svgs, ["Genome size and gene density overview", "Complete-assembly sensitivity comparison"]))
    (args.out / "index.html").write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Genome reference — redesigned figures</title><style>body{margin:0;background:#e8edef}main{max-width:1600px;margin:auto}section{margin:24px 0;background:#fbfcfc}svg{display:block;width:100%;height:auto}</style><main>' + panels + '</main></html>', encoding="utf-8")
    print(f"Saved two PNG/SVG figures and self-contained index.html in {args.out}")


if __name__ == "__main__":
    main()
