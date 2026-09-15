# Agentic Workshop

Building and employing agents for data analysis and visualization.

[Download the workshop ZIP](https://github.com/peterwadsackett/AgenticWorkshop/archive/refs/heads/main.zip) ·
[Quick start](#quick-start--download-extract-and-open) ·
[Project folders](#how-the-project-folder-works) ·
[Exercises](#exercises)

Use **OpenCode on your laptop** to work on the exercises. The DTU models run
on our servers; you do not need a cluster account, SSH, model downloads or
server-start commands.

## Quick start — download, extract and open

1. Install [OpenCode](https://opencode.ai/docs/#install) before the workshop.
   For this workshop, Windows users should install and run it inside WSL2.
   The terminal version is preferred; OpenCode Desktop is also supported.
2. Open [the workshop repository](https://github.com/peterwadsackett/AgenticWorkshop)
   and choose **Code → Download ZIP**.
3. Extract the ZIP and move the extracted folder wherever you want to work.
   Its default name is `AgenticWorkshop-main`.
4. In **OpenCode Desktop**, open that extracted folder as your project—the
   folder containing both `README.md` and `opencode.json`, not its parent.
   For the terminal version, run `opencode` from inside that folder.
5. Start a new chat. Open the model selector and choose a model under **DTU**.
   In the terminal version, type `/models`.

**No JSON editing, manual merging, API key or Custom provider setup is needed.**
Leave your existing global `opencode.jsonc`, `package.json` and
`node_modules` alone. OpenCode combines the project configuration with your
global settings automatically.

The workshop project shows one **DTU** group containing:

| Model | Context | Maximum output |
|---|---:|---:|
| Qwen 3.6 35B-A3B | 16384 | 4096 |
| Qwen 3.8 27B FP8 | 32768 | 4096 |
| Mistral Nemo 12B | 16384 | 4096 |
| GPT-OSS 20B | 16384 | 4096 |

GPT-OSS is the default model and handles small background tasks such as chat
titles. The DTU group is added alongside OpenCode's available free models
and your other configured providers. This file does not restrict the provider
list or change your global configuration. Other providers may require their
own sign-in or API key.

Keep exercise files in this folder. If you downloaded an earlier version,
download and open a fresh copy for the new configuration; keep your existing
exercise work. Fully quit and reopen OpenCode if it still shows the old list.

**Does opening the folder start the models?** No. It connects to models that
Peter and Dimitrios have already started. If a model is unavailable, ask an
organiser. You do not need server access.

See [OpenCode project configuration](https://opencode.ai/docs/config/#per-project).

## How the project folder works

Keep the extracted repository together. **OpenCode reads `.opencode/` for
project agents and skills**, while `opencode.json` in the repository root
contains the model connections, limits and permissions.

```text
AgenticWorkshop-main/
  opencode.json
  .opencode/
    agents/                  Agent definitions: <agent-name>.md
    skills/
      <skill-name>/
        SKILL.md             Reusable skill instructions
  exercises/
    01-skills/
    02-agents/
  mcp/                       Reserved for MCP-related materials
```

The agent and skill filenames above show where your definitions belong;
the starter folders currently contain only placeholders. A `.gitkeep`
file preserves a folder in Git and ZIP downloads; it is not an agent or skill.

The leading dot may hide `.opencode` in your file browser, but OpenCode can
still read it. Do not rename it, move it out of the project, or put
`opencode.json` inside it. Open the repository root, not `.opencode` itself.

The `exercises/` and `mcp/` folders organize workshop materials. Creating
an `mcp/` folder does not activate an MCP server.

See the OpenCode documentation for [agents](https://opencode.ai/docs/agents/)
and [skills](https://opencode.ai/docs/skills/).

## Exercises

Peter's [introduction and PDB-download skill exercise](workflow.md) is the
current starting point. The numbered exercise folders are prepared for
additional material; no exercise files have been added there yet.

## Manual connection reference — optional

<details>
<summary>Connection fields for a separate project without the supplied JSON</summary>

The ZIP method above is the workshop setup. These fields are only a fallback
for connecting in another project. The form creates separate providers; it
does not reproduce the single DTU group. There is no need to add these
separate providers when you already use the supplied workshop JSON.

Choose **Custom provider** and use the fields below. Create a separate
provider for each model you want. The connection type is **OpenAI-compatible**.

Use each Base URL exactly as shown, with no additional path at the end.
After entering the provider and model fields, select **Submit**.

The connection form may not offer context/output fields. If it does not,
set those limits in JSON using the instructions after the tables.
The supplied JSON already contains them.
See [OpenCode custom providers](https://opencode.ai/docs/providers/#custom-provider).

### Qwen 3.6 35B-A3B

| Field in OpenCode | What to enter |
|---|---|
| Provider ID | `dtu-qwen36` |
| Display name | `DTU Qwen 3.6` |
| Base URL | `https://teaching.healthtech.dtu.dk/workshop/qwen36` |
| API key | Leave empty |
| Models → Model ID | `qwen36` |
| Models → Display Name | `Qwen 3.6 35B-A3B` |
| Headers | Leave empty; do not add a header |
| Context limit, in JSON | `16384` |
| Output limit, in JSON | `4096` |

### Qwen 3.8 27B FP8

| Field in OpenCode | What to enter |
|---|---|
| Provider ID | `dtu-qwen38` |
| Display name | `DTU Qwen 3.8` |
| Base URL | `https://teaching.healthtech.dtu.dk/workshop/qwen38` |
| API key | Leave empty |
| Models → Model ID | `qwen38` |
| Models → Display Name | `Qwen 3.8 27B FP8` |
| Headers | Leave empty; do not add a header |
| Context limit, in JSON | `32768` |
| Output limit, in JSON | `4096` |

### Mistral Nemo 12B

| Field in OpenCode | What to enter |
|---|---|
| Provider ID | `dtu-mistral` |
| Display name | `DTU Mistral` |
| Base URL | `https://teaching.healthtech.dtu.dk/workshop/mistral` |
| API key | Leave empty |
| Models → Model ID | `mistral` |
| Models → Display Name | `Mistral Nemo 12B` |
| Headers | Leave empty; do not add a header |
| Context limit, in JSON | `16384` |
| Output limit, in JSON | `4096` |

### GPT-OSS 20B

| Field in OpenCode | What to enter |
|---|---|
| Provider ID | `dtu-gptoss` |
| Display name | `DTU GPT-OSS` |
| Base URL | `https://teaching.healthtech.dtu.dk/workshop/gptoss` |
| API key | Leave empty |
| Models → Model ID | `gptoss` |
| Models → Display Name | `GPT-OSS 20B` |
| Headers | Leave empty; do not add a header |
| Context limit, in JSON | `16384` |
| Output limit, in JSON | `4096` |


</details>

## Changing your context setting

Context is the space available for instructions, conversation, tool results
and the answer. Output is the maximum answer length, including reasoning.
Both are measured in tokens.

Only change context when an organiser tells you the server setting has changed.
In `opencode.json`, find the model under `provider → dtu → models → model ID`.
For Mistral, the limits look like this:

```json
{
  "name": "Mistral Nemo 12B",
  "limit": {
    "context": 16384,
    "output": 4096
  }
}
```

This is one model entry, not a complete OpenCode configuration. Save the file and
restart OpenCode. Increasing this number does not increase the server's capacity.

## If something does not work

| What you see | What to do |
|---|---|
| DTU models are missing | Check that OpenCode opened the folder containing `opencode.json`, then restart it. |
| Connection failed / 503 | Ask an organiser to check the model's start command. |
| Invalid API key / 401 | The workshop does not currently require a key; check for old provider settings. |
| Not found / 404 | Use a fresh workshop download; ask an organiser to check the URL if it persists. |
| Free models or other providers are missing | Check for `enabled_providers` or `disabled_providers` restrictions in your other project/global settings. The supplied workshop JSON does not hide them. |
| Too many requests / 429 | Wait briefly and try again; the servers are shared. |
| Context too long | Compact the conversation or start a new chat. |

Send Peter or Dimitrios the **model name and exact error message** if you need
help. Do not disable certificate checks or change server settings yourself.

OpenCode may ask to edit files or run commands **on your computer**. Review
those requests before allowing them. Work in the exercise folder.
When comparing models, start a fresh chat: switching models within a chat
can keep the earlier conversation and tool results.

---

For Peter and Dimitrios: [server administration and model settings](admin.md).
