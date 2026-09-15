# Testing the exercises

Keep loading checks separate from task results. A valid Markdown file, a model
reply, and a scientifically correct visualization are different milestones.

## Loading checks

From the repository folder, use `opencode agent list` to check agent discovery.
Use `opencode debug agent good-agent --pure` to inspect that example's resolved
settings, and `opencode debug skill --pure` to inspect skill discovery.
The `--pure` flag disables external plugins for this diagnostic, so it does not
test exercises that rely on those plugins. Do not publish unfiltered diagnostic
output from a personal configuration: it can contain local paths or private data.

These commands do not establish that any model can complete the exercise.

## Skill tests

Use a small, public or synthetic input. Check the actual output, including any
saved files. Try invalid input and a second valid input. For download skills,
separate HTTP success, successful parsing, and content checks. Computing a hash
locally records a fingerprint; verifying against a source checksum requires an
actual published checksum for the same file.

## Agent tests

Use the same model, prompt, tools, permissions, and iteration limit when comparing
instructions. Start fresh conversations in separate project copies. Record
model and OpenCode versions where available, settings, elapsed time, tool errors,
approval decisions, and any extra prompts or manual corrections. Repeat the
comparison and include a different input. A single successful run is not proof
of repeatability, and low temperature is not a guarantee of determinism.

For PDB visualization, check that the viewer opens, its controls work, identifiers
and selections match the input, and scientific statements have evidence. Have
a person inspect the rendering if no browser-inspection tool is available.

## Test record

Copy this table for each run. Leave untested checks marked **Not run**.

| Item | Record |
|---|---|
| Exercise, agent/skill version | |
| OpenCode version and model ID | |
| Input and expected result | |
| Settings and available tools | |
| Output folder | |
| Loading check | Not run |
| Normal input | Not run |
| Invalid/incomplete input | Not run |
| Different valid input | Not run |
| Browser checks, if relevant | Not run |
| Scientific/content review | Not run |
| Extra prompts and manual fixes | |
| Error messages and limitations | |

## Before demonstrating

Open the exact downloaded repository on a student-style setup and run the
exercise with the intended model. Keep a known-good output for comparison,
labelled with its model and settings. Check the chosen model is available
before the demonstration. Server startup and health checks are in
[admin.md](../admin.md); do not restart shared services as part of an exercise.
