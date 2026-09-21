#!/usr/bin/env python3
"""Reproducible genome example: standard library only; never invokes an LLM.

Agents own individual stages. `all` is an offline reference run, not a swarm.
"""
import argparse
import csv
import gzip
import hashlib
import html
import io
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
import statistics
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
DEFAULT_INPUT = ROOT / "exercises/03-mcp/data/byo/ncbi_reference_genomes.csv.gz"
SOURCE = "https://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt"
FIELDS = {"assembly_accession", "organism_name", "taxid", "assembly_level",
          "genome_size", "gc_percent", "seq_rel_date", "group", "total_gene_count"}
SUMMARY_FIELDS = ["cohort", "group", "assemblies", "valid_size_n", "valid_density_n",
                  "median_size_mb", "median_genes_per_mb"]
COMPARISON_FIELDS = ["group", "all_n", "complete_n", "all_size_mb", "complete_size_mb",
                     "size_change_pct", "all_density", "complete_density", "density_change_pct"]
EXPECTED_MODELS = {"coordinator": "opencode/big-pickle", "auditor": "dtu/mistral",
                   "analyst": "dtu/qwen36", "visualizer": "dtu/qwen38", "reviewer": "dtu/gptoss"}


def number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def load(path):
    raw = path.read_bytes()
    content = gzip.decompress(raw) if path.suffix == ".gz" else raw
    reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))
    if not FIELDS.issubset(reader.fieldnames or []):
        raise ValueError("Missing columns: " + ", ".join(sorted(FIELDS - set(reader.fieldnames or []))))
    rows = list(reader)
    if not rows:
        raise ValueError("Input has no data rows")
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError("Malformed CSV row")
    ids = [row["assembly_accession"].strip() for row in rows]
    if not all(ids) or len(set(ids)) != len(ids):
        raise ValueError("Missing or duplicate assembly accession")
    if any(not row["group"].strip() or not row["assembly_level"].strip() for row in rows):
        raise ValueError("Missing group or assembly level")
    return rows, hashlib.sha256(raw).hexdigest()


def write_text(path, content):
    # Exclusive creation keeps different runs and specialist results separate.
    with path.open("x", encoding="utf-8") as handle:
        handle.write(content)


def write_json(path, value):
    write_text(path, json.dumps(value, indent=2, allow_nan=False) + "\n")


def write_csv(path, fields, rows):
    with path.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def valid_size(row):
    size = number(row["genome_size"])
    return size if size is not None and size > 0 else None


def density(row):
    size, genes = valid_size(row), number(row["total_gene_count"])
    return genes * 1_000_000 / size if size is not None and genes is not None and genes >= 0 else None


def median(values):
    return statistics.median(values) if values else None


def audit(rows, sha, out):
    result = {
        "input_sha256": sha, "rows": len(rows), "unique_accessions": len(rows),
        "assembly_levels": dict(sorted(Counter(r["assembly_level"] for r in rows).items())),
        "groups": dict(sorted(Counter(r["group"] for r in rows).items())),
        "invalid_or_missing_size": sum(valid_size(r) is None for r in rows),
        "invalid_or_missing_density": sum(density(r) is None for r in rows),
        "units": {"genome_size": "base pairs", "reported_size": "megabases (1,000,000 bp)",
                  "total_gene_count": "annotated genes", "density": "genes per megabase"},
        "rules": ["Size must be finite and positive; gene count finite and non-negative.",
                  "Report separate denominators for size and gene density.",
                  "Median density is the median of assembly-level genes/Mb, not a ratio of medians.",
                  "Complete cohort means assembly_level exactly equals Complete Genome.",
                  "Reference assemblies are selected, not a random sample of organisms.",
                  "NCBI group labels mix taxonomic ranks; associations do not establish causation."]
    }
    write_json(out / "audit.json", result)


def require_audit(sha, out):
    info = json.loads((out / "audit.json").read_text())
    if info["input_sha256"] != sha:
        raise ValueError("Audit belongs to a different input; start a fresh run")


def analyze(rows, sha, out):
    require_audit(sha, out)
    groups = sorted({r["group"] for r in rows})
    summary = []
    for cohort in ("all", "complete"):
        grouped = defaultdict(list)
        for row in rows:
            if cohort == "all" or row["assembly_level"] == "Complete Genome":
                grouped[row["group"]].append(row)
        for group in groups:
            subset = grouped[group]
            sizes = [valid_size(r) / 1_000_000 for r in subset if valid_size(r) is not None]
            densities = [density(r) for r in subset if density(r) is not None]
            summary.append(dict(zip(SUMMARY_FIELDS, [cohort, group, len(subset), len(sizes),
                                 len(densities), median(sizes), median(densities)])))
    lookup = {(r["cohort"], r["group"]): r for r in summary}
    comparison = []
    for group in groups:
        a, c = lookup["all", group], lookup["complete", group]
        def change(key):
            return 100 * (c[key] / a[key] - 1) if a[key] not in (None, 0) and c[key] is not None else None
        comparison.append(dict(zip(COMPARISON_FIELDS, [group, a["assemblies"], c["assemblies"],
            a["median_size_mb"], c["median_size_mb"], change("median_size_mb"),
            a["median_genes_per_mb"], c["median_genes_per_mb"], change("median_genes_per_mb")])))
    write_csv(out / "summary.csv", SUMMARY_FIELDS, summary)
    write_csv(out / "comparison.csv", COMPARISON_FIELDS, comparison)
    write_json(out / "analysis.json", {"input_sha256": sha, "complete_filter": "assembly_level == 'Complete Genome'",
        "size_statistic": "median of positive finite genome_size / 1e6",
        "density_statistic": "median of finite nonnegative total_gene_count / (positive finite genome_size / 1e6)",
        "percent_change": "100 * (complete median / all median - 1); undefined if baseline is zero",
        "empty_cohorts": "count 0, blank median; never replace missing with zero"})


def svg_plot(summary, metric, label):
    groups = sorted({r["group"] for r in summary})
    values = [number(r[metric]) for r in summary]
    positive = [v for v in values if v is not None and v > 0]
    if not positive:
        return "<p>No positive values available for this log-scale plot.</p>"
    lo, hi = math.floor(math.log10(min(positive))), math.ceil(math.log10(max(positive)))
    if lo == hi:
        hi += 1
    left, width, top, step = 245, 590, 55, 52
    height = top + len(groups) * step + 65
    def x(value):
        return left + width * (math.log10(value) - lo) / (hi - lo)
    parts = [f'<svg viewBox="0 0 1000 {height}" role="img" aria-label="{html.escape(label)}: medians by group, logarithmic axis">',
             f'<title>{html.escape(label)} by group</title>',
             '<desc>Blue circles show all reference assemblies; orange squares show complete assemblies. Exact values and denominators are in the table below.</desc>']
    for exponent in range(lo, hi + 1):
        tick_x = x(10 ** exponent)
        parts += [f'<line x1="{tick_x}" y1="30" x2="{tick_x}" y2="{top + len(groups)*step}" stroke="#d5e0e8"/>',
                  f'<text x="{tick_x}" y="{height-25}" text-anchor="middle">{10**exponent:g}</text>']
    for i, group in enumerate(groups):
        y = top + i * step
        parts.append(f'<text x="225" y="{y+6}" text-anchor="end">{html.escape(group)}</text>')
        for cohort, offset, colour in (("all", -7, "#176aac"), ("complete", 7, "#b35008")):
            row = next(r for r in summary if r["group"] == group and r["cohort"] == cohort)
            value = number(row[metric])
            if value is not None and value > 0:
                title = html.escape(f'{group}, {cohort}: {value:.6g}; assemblies={row["assemblies"]}')
                if cohort == "all":
                    parts.append(f'<circle cx="{x(value)}" cy="{y+offset}" r="6" fill="{colour}"><title>{title}</title></circle>')
                else:
                    parts.append(f'<rect x="{x(value)-6}" y="{y+offset-6}" width="12" height="12" fill="{colour}"><title>{title}</title></rect>')
            else:
                parts.append(f'<text x="860" y="{y+offset+4}" font-size="11">{cohort}: missing/zero</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def visualize(out):
    rows = read_csv(out / "summary.csv")
    table = '<table><thead><tr>' + ''.join(f'<th>{html.escape(f)}</th>' for f in SUMMARY_FIELDS) + '</tr></thead><tbody>'
    for row in rows:
        table += '<tr>' + ''.join(f'<td>{html.escape(row[f]) if row[f] else "—"}</td>' for f in SUMMARY_FIELDS) + '</tr>'
    table += '</tbody></table>'
    content = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Genome size and gene density — workshop reference</title>
<style>body{font:17px system-ui,sans-serif;background:#f3f7fa;color:#173047;margin:0}main{max-width:1100px;margin:auto;padding:36px}h1{font-size:38px}h2{margin-top:38px}section{background:white;padding:24px;border-radius:10px;margin:20px 0}svg{width:100%;height:auto}svg text{font-family:system-ui,sans-serif;fill:#173047}table{border-collapse:collapse;font-size:12px;width:100%}th,td{padding:8px;border-bottom:1px solid #ccd8df;text-align:right}th:first-child,td:first-child,th:nth-child(2),td:nth-child(2){text-align:left}.scroll{overflow-x:auto}.blue{color:#176aac}.orange{color:#b35008}a{color:#176aac}</style>
<main><p>AGENTIC WORKSHOP · REPRODUCIBLE REFERENCE</p><h1>Genome size is not gene density</h1>
<p>Medians across NCBI RefSeq reference assemblies, grouped by NCBI category. Complete-assembly restriction is a sensitivity analysis, not a causal experiment.</p>
<p><span class="blue">● All assemblies</span> &nbsp; <span class="orange">■ Complete Genome only</span>. Both horizontal axes are logarithmic. Counts and valid-value denominators appear below.</p>'''
    for metric, label in (("median_size_mb", "Median genome size (Mb)"), ("median_genes_per_mb", "Median gene density (genes/Mb)")):
        content += f'<section><h2>{label}</h2>{svg_plot(rows, metric, label)}</section>'
    content += '<section><h2>Values and denominators</h2><p>Blank medians mean no valid observations, not zero. Gene density is calculated per assembly before taking its median. Non-positive medians cannot appear on a log axis.</p><div class="scroll">' + table + '</div></section>'
    content += f'<p>Source: <a href="{SOURCE}">NCBI RefSeq assembly summary</a>, workshop snapshot retrieved 18 September 2026. Selected reference assemblies, not all genomes. Group labels mix taxonomic ranks. See audit.json, comparison.csv, review.md and report.md alongside this file.</p></main></html>'
    write_text(out / "plots.html", content)


def show(value):
    return "—" if value is None or value == "" else f"{float(value):,.2f}"


def report(sha, out):
    checked = json.loads((out / "review.json").read_text())
    if checked.get("status") != "pass" or checked.get("input_sha256") != sha:
        raise ValueError("Independent review has not passed for this input")
    rows = read_csv(out / "comparison.csv")
    audit_info = json.loads((out / "audit.json").read_text())
    text = "# Genome size and gene density\n\n"
    text += "How do genome size and gene density differ across organism groups, and what changes when only complete assemblies are included?\n\n"
    text += f'The frozen reference subset contains **{audit_info["rows"]:,} assemblies**; **{audit_info["assembly_levels"].get("Complete Genome", 0):,}** are labelled Complete Genome. Size is in megabases; density is annotated genes per megabase.\n\n'
    text += "| Group | All n | Complete n | Median Mb, all → complete | Median genes/Mb, all → complete | Density change |\n|---|---:|---:|---|---|---:|\n"
    for row in rows:
        text += f'| {row["group"]} | {row["all_n"]} | {row["complete_n"]} | {show(row["all_size_mb"])} → {show(row["complete_size_mb"])} | {show(row["all_density"])} → {show(row["complete_density"])} | {show(row["density_change_pct"])}% |\n'
    ranked = sorted((r for r in rows if number(r["all_density"]) is not None), key=lambda r: float(r["all_density"]))
    if ranked:
        text += f'\nIn this subset, median density ranges from **{show(ranked[0]["all_density"])} genes/Mb ({ranked[0]["group"]})** to **{show(ranked[-1]["all_density"])} ({ranked[-1]["group"]})**. The complete-only column shows how the estimate moves when a different set of assemblies is selected.\n'
    text += "\n## Interpretation and limitations\n\n- Different denominators and selection matter: this is not a representative sample of species or all sequenced genomes.\n- The complete subset changes which assemblies and organisms are included. Differences cannot be attributed solely to improved assembly quality.\n- Group categories mix taxonomic ranks. No causal or mechanistic claim is established by these descriptive summaries.\n- Density is the median of assembly-level ratios, not the ratio of group medians. Valid size and density counts may differ; inspect summary.csv.\n- Missing complete-cohort medians remain missing. No result is invented for an empty group.\n\n## Reproduce and inspect\n\nOpen plots.html in a browser. The analysis rules are in analysis.json; audit.json records the input fingerprint and counts. Independent checks are in review.md. run.json distinguishes deterministic execution from actual model calls.\n\n"
    text += f"Source: {SOURCE} (snapshot retrieved 18 September 2026). Input SHA-256: `{sha}`. The fingerprint identifies this input; it is not a comparison to an NCBI-published checksum.\n"
    write_text(out / "report.md", text)
    write_json(out / "run.json", {"created_utc": datetime.now(timezone.utc).isoformat(), "input_sha256": sha,
        "execution": "deterministic Python reference pipeline", "llm_calls_by_this_script": 0,
        "configured_agent_models_not_evidence_of_calls": EXPECTED_MODELS,
        "independent_numerical_review": "pass", "browser_review": "not recorded by this script",
        "multi_agent_end_to_end": "not recorded by this script",
        "manual_output_corrections": [], "python": sys.version.split()[0]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["audit", "analyze", "visualize", "review", "report", "all"])
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    reference = ROOT / "exercises/02-agents/genome-demo/reference-output"
    if out != reference and not out.is_relative_to(ROOT / "outputs"):
        parser.error("Output must be a run folder under this project's outputs/, or the reference-output folder")
    if out == ROOT / "outputs":
        parser.error("Choose a named run folder, not outputs/ itself")
    try:
        rows, sha = load(args.input)
        if args.stage == "all" and out.exists():
            raise ValueError("Output folder already exists; choose a new run name")
        out.mkdir(parents=True, exist_ok=True)
        stages = ["audit", "analyze", "visualize", "review", "report"] if args.stage == "all" else [args.stage]
        for stage in stages:
            if stage == "audit":
                audit(rows, sha, out)
            elif stage == "analyze":
                analyze(rows, sha, out)
            elif stage == "visualize":
                require_audit(sha, out)
                visualize(out)
            elif stage == "review":
                subprocess.run([sys.executable, str(Path(__file__).with_name("verify_genomes.py")),
                                "--input", str(args.input), "--out", str(out)], check=True)
            else:
                report(sha, out)
            print(f"{stage}: completed — {out.name}")
    except (OSError, ValueError, KeyError, csv.Error, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Failed: {exc}\nNo existing outputs were deliberately overwritten. Use a fresh run folder after a failure.\n")


if __name__ == "__main__":
    main()
