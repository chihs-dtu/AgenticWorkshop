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

Create your own agent rather than changing the supplied examples. It can
visualize a structure, review an analysis, check a dataset, or perform another
task you can evaluate. Give it a specific job and a definition of success.

## Create the agent

Ask OpenCode to help create `.opencode/agents/my-agent.md`, or run
`opencode agent create` in your terminal and select the project location.
You can also write the Markdown file yourself. The filename becomes the
agent name. Keep your own agent separate from `bad-agent` and `good-agent`.

Start with a small definition like this:

```markdown
---
description: Checks a supplied analysis and reports evidence-backed findings
mode: primary
steps: 20
permission:
  edit: ask
  bash: ask
  task: deny
---

Inspect the supplied files and identify the question the analysis addresses.
Check assumptions against the data and available evidence.
Preserve original inputs and ask before changing analysis files.
Save the requested outputs in a separate folder.
Report the checks performed, findings, and unresolved limitations.
```

The YAML between `---` markers holds settings. The Markdown below it holds
the instructions. An agent is not a newly trained model: the same model can
run several agents with different instructions and permissions.

## Agent settings reference

This covers the named fields in OpenCode's published agent schema, checked
15 September 2026. Start with the first few fields; the remaining options
are available when you need them. Provider-specific options are open-ended,
so there is no universal list that every model accepts.

| Setting | What it changes | Example or caution |
|---|---|---|
| `description` | Explains the agent's job and when to choose it | A concrete task description, not just "helpful expert" |
| `mode` | Where the agent runs | `primary` for the main conversation, `subagent` for a helper, `all` for both |
| Markdown body / `prompt` | Instructions, decisions, expected outputs, and checks | Use the Markdown body in an agent file. In JSON, use `prompt` or `"prompt": "{file:./prompts/reviewer.txt}"` |
| `model` | Pins the agent to a provider/model | `dtu/gptoss`; leave unset to use the selected/default model or the calling agent's model |
| `variant` | Selects a configured model variant | Applies to the agent's configured model. Use a variant that actually exists |
| `steps` | Limits agentic iterations before a text-only response | Positive integer, such as `20`. It is not a token limit or an exact count of shell commands |
| `temperature` | Adjusts sampling randomness where supported | For example `0.2`; the valid range and effect depend on the model. Zero does not guarantee identical runs |
| `top_p` | Adjusts nucleus sampling where supported | For example `0.9`; usually vary this or temperature first, rather than both together |
| `permission` | Controls which tool actions run, ask, or stop | See the permission reference below |
| `disable` | Disables this agent | `true` or `false` |
| `hidden` | Hides a subagent from the `@` suggestion menu | For subagents only. This is not access control or a way to hide a solution file |
| `color` | Changes the agent's UI colour | A quoted hex colour such as `"#246B60"`, or a theme colour such as `accent` |
| `options` | Carries provider-specific model options | Verify the provider/adapter accepts each option. Do not assume DTU models accept another provider's settings |
| Extra provider fields | OpenCode can forward additional agent fields as model options | A misspelled field may be ignored or rejected downstream rather than caught as an agent error |
| `tools` | Legacy Boolean tool switches | Deprecated; use `permission` for new agents |
| `maxSteps` | Legacy iteration limit | Deprecated; use `steps` |

Schema: [OpenCode configuration](https://opencode.ai/config.json).
Usage: [agent configuration](https://opencode.ai/docs/agents/).

### Permissions and modular tools

Permission values are `allow` (run), `ask` (request approval), and `deny`
(block). Most omitted permissions are permissive, so omission is not a
safety restriction. Project/global permissions and agent overrides combine.
Available tools also depend on your installation and connected services.

| Permission key | Capability |
|---|---|
| `read` | Read file contents |
| `edit` | Modify files through the editing tools, including writes and patches |
| `glob`, `grep`, `list` | Find files, search content, and list directories when those tools are available |
| `bash` | Execute shell commands on your computer |
| `skill` | Load reusable skill instructions by skill name |
| `task` | Delegate to subagents by agent name/type |
| `webfetch`, `websearch` | Retrieve web content or search, when available |
| `lsp` | Query language-server information, when configured |
| `question` | Ask questions through the question tool, when available |
| `todowrite` | Maintain task lists when the tool is available |
| `external_directory` | Gate access to paths outside the project |
| `doom_loop` | Gate recovery from repeated identical tool calls |
| `*` | A general rule before more specific rules |
| A custom/MCP tool name or pattern | Control a tool exposed by an installed integration |

Pattern rules can restrict individual commands, files, skills, or subagents.
Use the catch-all first: the last matching rule wins. Not every permission
supports the same input-pattern semantics in every OpenCode version.

Example permission block, to replace the block in your own agent:

```yaml
permission:
  edit: ask
  bash:
    "*": ask
    "git status*": allow
    "git push*": deny
  skill:
    "*": deny
    "pdb-download": allow
  task: deny
  external_directory: ask
```

Replace `pdb-download` with the actual name of your installed skill. An allow
rule does not create a missing skill or force the agent to use it. Explain
when to load it in the Markdown body. A skill is guidance; scripts and other
tools perform the executable work.

To experiment with delegation, create a separate agent with `mode: subagent`
and replace `task: deny` in the main agent with a rule for that helper:

```yaml
task:
  "*": deny
  "structure-reviewer": ask
```

The helper needs its own definition and permissions. Delegation adds model
calls and can add latency. Begin with one agent before introducing helpers.

MCP tools require a server registered under `mcp` in `opencode.json`.
A permission rule or the `mcp/` folder alone does not connect a server.

Permissions are tool controls, not an operating-system sandbox. For example,
`edit: deny` does not make an agent read-only if `bash` can modify files.
Keep approval prompts enabled and review the requested action. Do not use
auto-approve mode when testing whether an `ask` rule behaves as intended.

References: [permissions](https://opencode.ai/docs/permissions/),
[skills](https://opencode.ai/docs/skills/), and
[MCP configuration](https://opencode.ai/docs/mcp-servers/).

### Settings that belong elsewhere

| Setting | Where it belongs |
|---|---|
| Context/output limits | `provider.dtu.models.<model-id>.limit.context` and `.limit.output` in `opencode.json` |
| Server context capacity | The administrator's model launch settings; a student JSON edit does not enlarge GPU capacity |
| Model URL and authentication | Provider configuration, not the agent instructions |
| Default chat and background models | Root `model` and `small_model` in `opencode.json` |
| Default agent | Root `default_agent` in `opencode.json` |
| Shared project rules | An `AGENTS.md` file or configured instruction files; these can affect several agents |
| MCP server connection | Root `mcp` configuration, with any required server software and credentials |

Leave the supplied DTU limits unchanged unless an organiser tells you the
server settings have changed. Do not add a made-up `context` field to agent
frontmatter or assume a raw API `max_tokens` field works there.

## Test your agent

1. Check that OpenCode discovers it. Outside the chat, run
   `opencode agent list`, or reopen the project and inspect the agent selector.
2. Try one normal task. Inspect the files and check the claimed results.
3. Try incomplete or invalid input. Does it explain the problem or invent an answer?
4. Try another input without rewriting the agent. Does it still work?
5. Change one instruction or setting, start a fresh chat, and compare again.

Record the agent version, model ID, settings, inputs, tool access, output
folder, and checks. Repeat trials when comparing quality. Low temperature
alone cannot control model/backend changes, tool results, or conversation
history. A successfully parsed configuration is only a loading test.

For PDB viewers, inspect the browser output yourself unless the agent has
actually used a browser inspection tool. Keep "code generated", "viewer
opened", "controls checked", and "scientific content verified" distinct.
