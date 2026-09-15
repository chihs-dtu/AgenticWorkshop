# Exercise 2a — From a basic agent to a good agent

An agent can complete a task without completing it particularly well.
These initial examples compare a vague instruction with an explicit,
verifiable workflow. PDB visualization is the first case, not the scope
of every exercise in this repository.

## The two agents

| Agent | What changes |
|---|---|
| [bad-agent](../../.opencode/agents/bad-agent.md) | A plausible but underspecified request to build a viewer. It is not instructed to make mistakes. |
| [good-agent](../../.opencode/agents/good-agent.md) | Inspects the input, chooses useful views, reuses available skills, records provenance, and checks the result. |

Both are primary agents with the same permissions and 20-step limit. Neither
hardcodes a model or temperature. They are first-iteration teaching examples,
not a tested guarantee of better results or the completed reference visualizer.

## Try the same request

Open the repository in OpenCode and start a fresh chat. In the terminal,
use Tab to select `bad-agent`; in Desktop, use the agent selector. Reopen
OpenCode if the newly added agents do not appear.

Use this request:

> Create an interactive browser visualization of PDB 4HHB that I can use to
> explain the structure to another researcher. Save everything under
> outputs/bad-agent. I have a browser and OpenCode; do not require additional
> software installation. Briefly explain how to open and use the result.

Start another fresh chat, select `good-agent`, and repeat the same request,
changing only the output folder to `outputs/good-agent`.

Keep the model, input, available skills/tools, and approval decisions the same.
Do not give the second agent the first agent's output. For a stricter comparison,
use separate extracted copies of the repository so neither can inspect the
other's files. The good example is included here for inspection; it is not hidden
from students or their agents.

## Inspect, improve, and reuse

- Does the structure actually load, and do the controls work?
- Are chains, selected residues, and any ligands identified correctly?
- Is the view useful for explaining the structure, with readable labels?
- Are its scientific claims supported, and are limitations visible?
- Can someone reproduce the view and load a different structure?
- What manual corrections and extra prompts were necessary?

Edit or create an agent of your own and repeat the comparison on another
structure. Judge the generated files and behaviour, not the agent's claim
that it succeeded. One run does not establish a fixed performance difference.

# Exercise 2b — From a good agent to your agent
