# Independent numerical review

Status: **pass**.

Independent CSV parsing, Decimal arithmetic, explicit sorted median; does not import analyzer.

- PASS: Exactly one summary per group/cohort
- PASS: Recomputed counts and medians: all/archaea
- PASS: Recomputed counts and medians: all/bacteria
- PASS: Recomputed counts and medians: all/fungi
- PASS: Recomputed counts and medians: all/invertebrate
- PASS: Recomputed counts and medians: all/plant
- PASS: Recomputed counts and medians: all/protozoa
- PASS: Recomputed counts and medians: all/vertebrate_mammalian
- PASS: Recomputed counts and medians: all/vertebrate_other
- PASS: Recomputed counts and medians: complete/archaea
- PASS: Recomputed counts and medians: complete/bacteria
- PASS: Recomputed counts and medians: complete/fungi
- PASS: Recomputed counts and medians: complete/invertebrate
- PASS: Recomputed counts and medians: complete/plant
- PASS: Recomputed counts and medians: complete/protozoa
- PASS: Recomputed counts and medians: complete/vertebrate_mammalian
- PASS: Recomputed counts and medians: complete/vertebrate_other
- PASS: Exactly one comparison per group
- PASS: Recomputed complete-only comparison: archaea
- PASS: Recomputed complete-only comparison: bacteria
- PASS: Recomputed complete-only comparison: fungi
- PASS: Recomputed complete-only comparison: invertebrate
- PASS: Recomputed complete-only comparison: plant
- PASS: Recomputed complete-only comparison: protozoa
- PASS: Recomputed complete-only comparison: vertebrate_mammalian
- PASS: Recomputed complete-only comparison: vertebrate_other
- PASS: Audit fingerprint matches source
- PASS: Row and unique assembly counts
- PASS: Audit group counts
- PASS: Audit assembly-level counts
- PASS: Invalid/missing size count
- PASS: Invalid/missing density count

## Limits of this review

- Numerical consistency is not evidence for causal biology.
- This checker does not inspect browser appearance or record model execution.
