# Genome-size demonstration

> **Status, 21 September 2026:** the supplied numerical reference is generated
> and independently checked. The five OpenCode definitions are supplied for
> rehearsal, but the complete multi-model run is **not yet validated**: all four
> public DTU model routes returned HTTP 503, and compute04 has a driver/library
> mismatch. Do not present these saved files as outputs of a completed swarm.

## Question

How do genome size and gene density differ across organism groups, and how
does restricting the analysis to complete assemblies change the conclusions?

Use the existing [NCBI reference subset](../../03-mcp/data/byo/PROVENANCE.md#ncbi_reference_genomescsvgz).
One row is an assembly, not a species. The reference set is selected rather
than a random sample. Size is measured in base pairs; report Mb using 1,000,000
bp. Calculate genes/Mb per assembly before taking a group median.

## Five agents, five models

| Agent | Model | Owns |
|---|---|---|
| `genome-coordinator` | `opencode/big-pickle` | Final report, handoffs and actual agent-run notes |
| `genome-auditor` | `dtu/mistral` | `audit.json`: units, counts, missingness and source fingerprint |
| `genome-analyst` | `dtu/qwen36` | `summary.csv`, `comparison.csv`, `analysis.json` |
| `genome-visualizer` | `dtu/qwen38` | `plots.html`: log-scale plots and exact-value table |
| `genome-reviewer` | `dtu/gptoss` | `review.json`, `review.md`: independent recalculation and limitations |

Definitions live in the repository-root `.opencode/agents/`. The coordinator
uses `mode: primary`; the specialists use `mode: subagent`. Every specialist
has `task: deny`; only the coordinator can delegate to the four named agents.
They are separate model sessions, not one shared conversation or pooled context.

Big Pickle is an external free offer, subject to availability. Do not quietly
substitute a paid model. Check `/models` and your provider access first.
Use public data: prompts and retrieved results sent to an external model leave
your laptop. No passwords or personal data belong in the task.

## Run with OpenCode

This example needs **Python 3.10 or later**, available as `python3` in your
terminal (`python3 --version`). Windows: use WSL2. No Python packages, MCP,
database setup or web server are needed. If Python is missing, ask an organiser
before installing anything. Leave the MCP servers off.

Open the workshop root and select `genome-coordinator`. Start a fresh chat:

> Answer the genome-size demonstration question using your four specialist
> subagents, each on its configured model. Use the supplied NCBI dataset and
> save this run in outputs/genome-demo/run-01. Read the genome-demo guide.
> Do not copy the reference answers. Report every failed or untested step.

Approve only the intended commands. The reference agents ask before shell
commands and file edits. If an approval is denied, the coordinator must report
the missing work. Do not enable global auto-approval merely to avoid prompts.

The dependency order is **audit → analysis → visualization and review → report**.
Visualization and review can overlap because they write different files. The
two-worker limit is an instruction, not a guaranteed scheduler cap. More agents
do not imply that every job should run simultaneously on shared model servers.

Workers receive explicit input/output paths and concise findings. They do not
automatically know another agent's conversation. Missing dependencies, an
unavailable model or a failed review must stop the affected handoff. One focused
correction round uses a new run folder rather than overwriting the failure.

Open `plots.html` in a browser, read `report.md`, and inspect `agent-run.md`.
That last file must describe actual delegations and failures, not merely repeat
the model configuration. `run.json` records the Python execution only.

## What the supplied computational tools do

The agents use a small, deterministic script for their own stage. This makes
numerical errors testable while leaving planning, handoffs and interpretation
visible. The scripts do **not** call models or create subagents.

Run from the workshop root, using the same new output folder throughout:

```bash
python3 exercises/02-agents/genome-demo/scripts/genome_demo.py audit --out outputs/genome-demo/manual-01
python3 exercises/02-agents/genome-demo/scripts/genome_demo.py analyze --out outputs/genome-demo/manual-01
python3 exercises/02-agents/genome-demo/scripts/genome_demo.py visualize --out outputs/genome-demo/manual-01
python3 exercises/02-agents/genome-demo/scripts/genome_demo.py review --out outputs/genome-demo/manual-01
python3 exercises/02-agents/genome-demo/scripts/genome_demo.py report --out outputs/genome-demo/manual-01
```

For a one-command **offline reference run**, not an agent-team demonstration:

```bash
python3 exercises/02-agents/genome-demo/scripts/genome_demo.py all --out outputs/genome-demo/offline-01
```

Use a new run name each time. Existing output files are never overwritten.
No dependencies are installed and no source data is downloaded. An alternative
`--input` must have the genome schema; penguins and proteins need their own
adapted analysis tools, not just a different input filename.

## Inspect the saved reference

- [Redesigned Python figures](reference-output/redesigned/index.html) — paired median overview and complete-assembly percentage changes, with sample counts. [Overview PNG](reference-output/redesigned/genome-overview.png) · [Comparison PNG](reference-output/redesigned/complete-assembly-shift.png).
- [Plots](reference-output/plots.html) — download/open locally; GitHub shows HTML source.
- [Report](reference-output/report.md), [summary](reference-output/summary.csv) and [comparison](reference-output/comparison.csv).
- [Independent numerical review](reference-output/review.md).
- [Run record](reference-output/run.json) and [rehearsal status](reference-output/rehearsal.md).

The redesigned figures are an optional **Matplotlib** rendering of the already
verified reference tables. They do not change the calculations or require MCP.
PNG, editable SVG and a self-contained HTML view are supplied. The original
standard-library agent pipeline remains available without extra packages.
To reproduce the redesign in a Python environment with Matplotlib installed:

```bash
python3 exercises/02-agents/genome-demo/scripts/plot_genomes.py --input exercises/02-agents/genome-demo/reference-output --out outputs/genome-demo/redesign-01
```

Use a new output directory. This layout and its captions are specific to the
supplied reference dataset; adapt them before using a different dataset.

Important observations to check yourself: only 7,268 of the 25,965 assemblies
are complete; some groups have only three complete assemblies. The complete
subset changes which organisms are represented. It does not isolate the
causal effect of assembly quality. A dramatic percentage change with three
observations needs a different interpretation from one with thousands.

The reviewer recomputes from the original CSV with a separate Decimal-based
implementation. It does not import the analyst's median function. Run the
offline regression checks with:

```bash
python3 -m unittest discover -s exercises/02-agents/genome-demo/scripts -p 'test_*.py' -v
```

These checks cover missing/invalid values, duplicates, empty cohorts, changed
inputs, overwrite protection, independent detection of altered results and
SVG escaping. They do not prove that any model can complete the workflow.
Before the live demonstration, run the team from a clean project copy, check
each specialist's actual model, inspect the browser result and repeat a run.
Record manual corrections and failed/denied actions beside that run.

Return to [Exercise 2c](../README.md#exercise-2c--a-team-of-specialists).
