"""Offline checks for the reference implementation; no model calls."""
import csv
import gzip
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

import genome_demo as demo
import verify_genomes as independent


class GenomeTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name)
        self.source = self.root / "input.csv.gz"
        self.out = self.root / "results"
        self.out.mkdir()
        self.rows = [self.row("a", "A", "Complete Genome", "1000000", "1000"),
                     self.row("b", "A", "Contig", "2000000", "100"),
                     self.row("c", "B", "Scaffold", "NA", "20"),
                     self.row("d", "B", "Scaffold", "3000000", ""),
                     self.row("e", "B", "Contig", "-1", "10")]
        self.save()

    def row(self, name, group, level, size, genes):
        return dict(assembly_accession=name, organism_name="test", taxid="1", assembly_level=level,
                    genome_size=size, gc_percent="50", seq_rel_date="2020-01-01", group=group, total_gene_count=genes)

    def save(self):
        with gzip.open(self.source, "wt", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=sorted(demo.FIELDS))
            writer.writeheader()
            writer.writerows(self.rows)

    def pipeline(self):
        rows, sha = demo.load(self.source)
        demo.audit(rows, sha, self.out)
        demo.analyze(rows, sha, self.out)
        return independent.verify(self.source, self.out)

    def test_values_and_empty_cohorts(self):
        self.assertEqual(self.pipeline()["status"], "pass")
        result = {(r["cohort"], r["group"]): r for r in demo.read_csv(self.out / "summary.csv")}
        self.assertEqual(float(result["all", "A"]["median_genes_per_mb"]), 525)
        self.assertEqual(float(result["complete", "A"]["median_genes_per_mb"]), 1000)
        self.assertEqual(result["complete", "B"]["assemblies"], "0")
        self.assertEqual(result["complete", "B"]["median_size_mb"], "")
        self.assertEqual(result["all", "B"]["valid_density_n"], "0")

    def test_reviewer_detects_tampering(self):
        self.pipeline()
        path = self.out / "summary.csv"
        content = path.read_text().replace("525.0", "999.0")
        path.write_text(content)
        self.assertEqual(independent.verify(self.source, self.out)["status"], "fail")

    def test_duplicate_id_rejected(self):
        self.rows[1]["assembly_accession"] = "a"
        self.save()
        with self.assertRaisesRegex(ValueError, "duplicate"):
            demo.load(self.source)

    def test_missing_header_rejected(self):
        path = self.root / "bad.csv"
        path.write_text("foo\nbar\n")
        with self.assertRaisesRegex(ValueError, "Missing columns"):
            demo.load(path)

    def test_empty_input_rejected(self):
        self.rows = []
        self.save()
        with self.assertRaisesRegex(ValueError, "no data"):
            demo.load(self.source)

    def test_nonfinite_excluded_and_zero_genes_valid(self):
        self.rows[0]["genome_size"] = "inf"
        self.rows[1]["total_gene_count"] = "0"
        self.save()
        self.assertEqual(self.pipeline()["status"], "pass")
        self.assertIsNone(demo.number("NaN"))
        self.assertEqual(demo.density(self.rows[1]), 0)

    def test_source_change_rejected(self):
        rows, sha = demo.load(self.source)
        demo.audit(rows, sha, self.out)
        with self.assertRaisesRegex(ValueError, "different input"):
            demo.analyze(rows, "wrong-fingerprint", self.out)

    def test_existing_output_not_overwritten(self):
        self.pipeline()
        before = (self.out / "summary.csv").read_bytes()
        rows, sha = demo.load(self.source)
        with self.assertRaises(FileExistsError):
            demo.analyze(rows, sha, self.out)
        self.assertEqual(before, (self.out / "summary.csv").read_bytes())

    def test_svg_well_formed_and_html_escaped(self):
        self.rows[0]["group"] = "<test&group>"
        self.save()
        self.pipeline()
        rows = demo.read_csv(self.out / "summary.csv")
        svg = demo.svg_plot(rows, "median_size_mb", "Size")
        ET.fromstring(svg)
        self.assertNotIn("<test&group>", svg)
        demo.visualize(self.out)
        page = (self.out / "plots.html").read_text()
        self.assertIn("&lt;test&amp;group&gt;", page)
        self.assertNotIn("<script", page)

    def test_fingerprint_matches_bytes(self):
        _, sha = demo.load(self.source)
        self.assertEqual(sha, hashlib.sha256(self.source.read_bytes()).hexdigest())

    def test_report_requires_pass(self):
        demo.write_json(self.out / "review.json", {"status": "fail", "input_sha256": "bad"})
        with self.assertRaisesRegex(ValueError, "not passed"):
            demo.report("bad", self.out)


if __name__ == "__main__":
    unittest.main()
