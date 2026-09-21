# Genome size and gene density

How do genome size and gene density differ across organism groups, and what changes when only complete assemblies are included?

The frozen reference subset contains **25,965 assemblies**; **7,268** are labelled Complete Genome. Size is in megabases; density is annotated genes per megabase.

| Group | All n | Complete n | Median Mb, all → complete | Median genes/Mb, all → complete | Density change |
|---|---:|---:|---|---|---:|
| archaea | 832 | 432 | 3.18 → 2.80 | 1,024.40 → 1,035.18 | 1.05% |
| bacteria | 22736 | 6745 | 4.16 → 3.88 | 934.25 → 934.24 | -0.00% |
| fungi | 668 | 69 | 32.83 → 23.03 | 350.51 → 364.31 | 3.94% |
| invertebrate | 512 | 3 | 386.70 → 327.38 | 45.66 → 45.38 | -0.63% |
| plant | 211 | 9 | 639.59 → 393.33 | 63.51 → 84.14 | 32.50% |
| protozoa | 115 | 4 | 31.22 → 23.17 | 280.66 → 278.12 | -0.91% |
| vertebrate_mammalian | 269 | 3 | 2,576.50 → 3,060.04 | 12.45 → 14.33 | 15.04% |
| vertebrate_other | 622 | 3 | 1,143.90 → 1,261.97 | 20.65 → 36.96 | 79.01% |

In this subset, median density ranges from **12.45 genes/Mb (vertebrate_mammalian)** to **1,024.40 (archaea)**. The complete-only column shows how the estimate moves when a different set of assemblies is selected.

## Interpretation and limitations

- Different denominators and selection matter: this is not a representative sample of species or all sequenced genomes.
- The complete subset changes which assemblies and organisms are included. Differences cannot be attributed solely to improved assembly quality.
- Group categories mix taxonomic ranks. No causal or mechanistic claim is established by these descriptive summaries.
- Density is the median of assembly-level ratios, not the ratio of group medians. Valid size and density counts may differ; inspect summary.csv.
- Missing complete-cohort medians remain missing. No result is invented for an empty group.

## Reproduce and inspect

Open plots.html in a browser. The analysis rules are in analysis.json; audit.json records the input fingerprint and counts. Independent checks are in review.md. run.json distinguishes deterministic execution from actual model calls.

Source: https://ftp.ncbi.nlm.nih.gov/genomes/refseq/assembly_summary_refseq.txt (snapshot retrieved 18 September 2026). Input SHA-256: `77c8e536f597288a7277871fb4e2ebcc8c76a0608ff350d2c1ae2312cbe4128c`. The fingerprint identifies this input; it is not a comparison to an NCBI-published checksum.
