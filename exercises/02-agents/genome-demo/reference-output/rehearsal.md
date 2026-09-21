# Reference run — 21 September 2026

## What produced these files

The supplied Python reference runner processed the repository's frozen NCBI
reference-genome CSV. **No LLM generated these saved numerical outputs.**
The code was developed for the exercise; the generated result files were not
manually corrected. `run.json` identifies the input fingerprint and execution.

| Check | Result |
|---|---|
| Offline regression tests | 11 passed, including tampered-result detection and empty cohorts |
| Independent numerical recomputation | 32 checks passed using separate Decimal arithmetic |
| Repeated computation | Same deterministic artifacts; run timestamp is intentionally different |
| Fresh-copy execution | Passed with the data and scripts copied to a separate project |
| ZIP extraction | Packaged the pending repository changes, extracted into a fresh folder, reran the reference pipeline successfully and confirmed coordinator discovery |
| OpenCode configuration | All five reference agents discovered in OpenCode 1.18.30 with their intended models |
| Team activation | Team-prefixed files were not discovered in the exercise folder; all five were discovered after copying into `.opencode/agents/` |
| Browser rendering | Opened in Chrome through a localhost-only preview; both log-scale charts, group labels, legends and numerical table inspected |
| Direct `file://` opening | Not separately verified; the HTML is self-contained, with no script, font or image downloads |
| Live five-model team | **Blocked / not run successfully**: all four public DTU model routes returned HTTP 503 |
| Larger server contexts | **Not applied**: compute04 has an NVIDIA driver/library mismatch; targets remain unvalidated |

Initial configured models: coordinator `opencode/big-pickle`, auditor
`dtu/mistral`, analyst `dtu/qwen36`, visualizer `dtu/qwen38`, reviewer
`dtu/gptoss`. Configuration is not proof of a successful call to those models.

The next live rehearsal must verify actual delegation and model selection,
failed/denied actions, the final interpretation and a repeated run. Save that
run separately with its manual interventions; do not relabel this deterministic
reference as a live agent result.
