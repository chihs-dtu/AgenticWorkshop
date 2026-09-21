#!/usr/bin/env python3
"""Independent Decimal-based checks; deliberately does not import the analyzer."""
import argparse
import csv
from decimal import Decimal, InvalidOperation
import gzip
import hashlib
import json
from pathlib import Path


def parse_number(value):
    try:
        value = Decimal(value)
        return value if value.is_finite() else None
    except (InvalidOperation, TypeError, ValueError):
        return None


def middle(values):
    values = sorted(values)
    n = len(values)
    if not n:
        return None
    return values[n // 2] if n % 2 else (values[n // 2 - 1] + values[n // 2]) / 2


def verify(source, out):
    opener = gzip.open if source.suffix == ".gz" else open
    with opener(source, "rt", encoding="utf-8-sig", newline="") as stream:
        raw = list(csv.DictReader(stream))
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    failures = []
    checks = []
    def check(ok, name):
        checks.append({"check": name, "passed": bool(ok)})
        if not ok:
            failures.append(name)
    def close(actual, expected):
        if expected is None:
            return actual == ""
        value = parse_number(actual)
        return value is not None and abs(value - expected) <= max(abs(expected), Decimal(1)) * Decimal("1e-9")

    with (out / "summary.csv").open(newline="") as stream:
        summaries = list(csv.DictReader(stream))
    expected = {}
    groups = sorted({r["group"] for r in raw})
    for group in groups:
        for cohort in ("all", "complete"):
            rows = [r for r in raw if r["group"] == group and
                    (cohort == "all" or r["assembly_level"] == "Complete Genome")]
            sizes, densities = [], []
            for row in rows:
                size = parse_number(row["genome_size"])
                genes = parse_number(row["total_gene_count"])
                if size is not None and size > 0:
                    sizes.append(size / 1_000_000)
                    if genes is not None and genes >= 0:
                        densities.append(genes * 1_000_000 / size)
            expected[cohort, group] = {"assemblies": Decimal(len(rows)), "valid_size_n": Decimal(len(sizes)),
                "valid_density_n": Decimal(len(densities)), "median_size_mb": middle(sizes),
                "median_genes_per_mb": middle(densities)}
    keys = [(r["cohort"], r["group"]) for r in summaries]
    check(len(keys) == len(set(keys)) and set(keys) == set(expected), "Exactly one summary per group/cohort")
    for row in summaries:
        key = row["cohort"], row["group"]
        if key in expected:
            check(all(close(row[k], v) for k, v in expected[key].items()), f"Recomputed counts and medians: {key[0]}/{key[1]}")
    with (out / "comparison.csv").open(newline="") as stream:
        comparisons = list(csv.DictReader(stream))
    check(len(comparisons) == len(groups) and {r["group"] for r in comparisons} == set(groups), "Exactly one comparison per group")
    for row in comparisons:
        group = row["group"]
        if group not in groups:
            continue
        a, c = expected["all", group], expected["complete", group]
        values = {"all_n": a["assemblies"], "complete_n": c["assemblies"],
                  "all_size_mb": a["median_size_mb"], "complete_size_mb": c["median_size_mb"],
                  "all_density": a["median_genes_per_mb"], "complete_density": c["median_genes_per_mb"]}
        for result, key in (("size_change_pct", "median_size_mb"), ("density_change_pct", "median_genes_per_mb")):
            values[result] = 100 * (c[key] / a[key] - 1) if a[key] not in (None, 0) and c[key] is not None else None
        check(all(close(row[k], v) for k, v in values.items()), f"Recomputed complete-only comparison: {group}")
    audit = json.loads((out / "audit.json").read_text())
    check(audit["input_sha256"] == sha, "Audit fingerprint matches source")
    check(audit["rows"] == len(raw) == len({r["assembly_accession"] for r in raw}), "Row and unique assembly counts")
    check(audit["groups"] == {g: sum(r["group"] == g for r in raw) for g in groups}, "Audit group counts")
    levels = {r["assembly_level"] for r in raw}
    check(audit["assembly_levels"] == {level: sum(r["assembly_level"] == level for r in raw) for level in levels}, "Audit assembly-level counts")
    check(audit["invalid_or_missing_size"] == len(raw) - sum(int(v["valid_size_n"]) for (c, _), v in expected.items() if c == "all"), "Invalid/missing size count")
    check(audit["invalid_or_missing_density"] == len(raw) - sum(int(v["valid_density_n"]) for (c, _), v in expected.items() if c == "all"), "Invalid/missing density count")
    return {"status": "pass" if not failures else "fail", "input_sha256": sha,
            "method": "Independent CSV parsing, Decimal arithmetic, explicit sorted median; does not import analyzer",
            "checks": checks, "failures": failures,
            "limitations": ["Numerical consistency is not evidence for causal biology.",
                            "This checker does not inspect browser appearance or record model execution."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify(args.input, args.out)
        with (args.out / "review.json").open("x") as stream:
            json.dump(result, stream, indent=2)
            stream.write("\n")
        with (args.out / "review.md").open("x") as stream:
            stream.write("# Independent numerical review\n\nStatus: **" + result["status"] + "**.\n\n" + result["method"] + ".\n\n")
            for row in result["checks"]:
                stream.write(f'- {"PASS" if row["passed"] else "FAIL"}: {row["check"]}\n')
            stream.write("\n## Limits of this review\n\n" + "\n".join("- " + s for s in result["limitations"]) + "\n")
        if result["status"] != "pass":
            parser.exit(1, "Independent numerical review failed\n")
        print(f'Independent numerical review passed: {len(result["checks"])} checks')
    except (OSError, ValueError, KeyError, csv.Error) as exc:
        parser.exit(1, f"Review could not finish: {exc}\n")


if __name__ == "__main__":
    main()
