# Agentic Workshop

Building and employing agents for data analysis and visualization.

OpenCode offers a changing selection of AI Large Language Models free of charge. We have also
prepared **four locally hosted DTU LLM models** for this workshop. You can use
either option, or connect your own supported subscriptions or API accounts.
A paid subscription is not required to participate.

[Download the workshop ZIP](https://github.com/peterwadsackett/AgenticWorkshop/archive/refs/heads/main.zip) ·
[Quick start](#quick-start--download-extract-and-open) ·
[Exercises](#exercises)

Use **OpenCode on your laptop** to work on the exercises. The DTU models run
on our server cluster; you do not need a cluster account, SSH, model downloads or
server-start commands.

Install from your terminal: `npm install -g @opencode/cli`

> **This workshop has moved to OpenCode v2.** v2 ships as a different package,
> `@opencode/cli`, so the old `curl -fsSL https://opencode.ai/install | bash`
> installs v1 and will not match these materials. Install with
> `npm install -g @opencode/cli` and check `opencode --version` reports 2.x.
>
> If you already have v1, remove it first. On Homebrew that is
> `brew uninstall opencode`. Avoid `opencode uninstall`: it removes all related
> files, including your global configuration and saved credentials.
>
> Some commands changed. `opencode agent list` is now `opencode debug agents`,
> `opencode web` is now `opencode serve`, and `opencode debug skill` is gone;
> use `/skills` in the chat instead.

## Before the exercises: three pieces of advice in a lesson format

### Lesson one — you are in charge of your data

Every prompt you send goes somewhere. Where depends on the model you picked
in the selector, and the difference matters before you paste anything real
into a chat.

| What you choose | Where your data goes |
|---|---|
| **DTU models** | Stays on our server, inside the DTU network |
| **Free models** | Leaves our network to a third party. Free offers are commonly paid for with your data and your interaction with the model |
| **Your own subscription** (Codex, Claude, others) | Depends on that provider, and on whether you have opted out of having your data used for training |

User discretion is advised at all times. You are in charge of your data, you
are in charge of the permissions you give your models, and you are in charge
of which data you put in front of them. Nothing in this workshop removes that
responsibility from you, and no default setting decides it for you.

Use public data with external models. Keep anything confidential or personal
on the DTU models, or off the machine entirely.

### Lesson two — `/compact` is your friend

A conversation has a fixed budget. Everything counts against it: your
messages, the model's replies, file contents it has read, and every tool
result it has seen. When the budget runs out mid-task, the run stops being
useful.

`/compact` summarises the conversation so far and continues with the summary
in place of the raw history. You keep the thread, you get the room back.

Get to know it early, on a conversation you do not mind losing, rather than
discovering it when you are deep in an exercise. The sooner the better.

### Lesson three — use `/theme` before anything else to look cool (in front of your PI) and personalise your experience

Opencode (v1 and v2) harnesses comes with their own preinstalled themes. Pick one 
that inspires you to finish this workshop (hint: maybe `matrix` will do the trick).

## Quick start — download, extract and open

1. Install [OpenCode](https://opencode.ai/docs/#install) before the workshop.
   For this workshop, Windows users should install and run it inside WSL2.
   The terminal version (CLI) is preferred; OpenCode Desktop is also supported, however the CLI can function as
   a desktop version in a browser at no extra cost.
2. For Linux and WSL2 Ubunbu (Linux) it is this command for install OpenCode CLI (terminal)<br>
   `npm install -g @opencode/cli` 
3. Open [the workshop repository](https://github.com/peterwadsackett/AgenticWorkshop)
   and choose **Code → Download ZIP**.
4. Extract the ZIP and move the extracted folder wherever you want to work.
   Its default name is `AgenticWorkshop-main`. You can rename it if you prefer;
   nothing here depends on the name. The text calls it the workshop root, and
   every path you will type is relative to it.
5. In **OpenCode Desktop**, open that extracted folder as your project—the
   folder containing both `README.md` and `opencode.json`, not its parent.
   For the terminal version, run `opencode` from inside that folder, or
   `opencode serve` for the browser version.
6. Start a new chat. Open the model selector and choose a model under **DTU**.
   In the terminal version, type `/models`.

**For the supplied DTU models, no JSON editing, manual merging, API key or
Custom provider setup is needed.**

Exercise 3 additionally needs [`uv`](https://docs.astral.sh/uv/) installed
(`curl -LsSf https://astral.sh/uv/install.sh | sh`, inside WSL2 on Windows).
Sharing in Exercises 2c and 4 needs a GitHub account and Git, or GitHub's
browser upload interface. [`gh`](https://cli.github.com/) is optional.
Ask an organiser if you prefer to hand over your files without an account.

Exercise **2c** also needs Python **3.10 or later** (`python3 --version`),
with no additional Python packages. Team sharing needs GitHub access; a
coordinator can download the reviewed files as a ZIP to run them locally.

Leave your existing global `opencode.jsonc`, `package.json` and
`node_modules` alone. OpenCode combines the project configuration with your
global settings automatically.

## LLM Models you can use
First be aware of the pricing - it can be creative.
* Free models - your data and behavior is logged and used by the provider
* Paid models - often subscription-based. Maybe as safe and confidential as the provider says
* Local models - running on your own hardware. As confidential as your system
* DTU models - free for the workshop. We do not store/use/abuse your data. Trust us......
### Our four DTU models
<details>
<summary>Model list</summary>

The workshop project shows one **DTU** group containing:

| Model | Context | Maximum output | Description |
|---|---:|---:|---:|
| GPT-OSS 20B | 16384 | 4096 | Default model, handles small background tasks
| Mistral Nemo 12B | 16384 | 4096 | French model
| Qwen 3.6 35B-A3B | 16384 | 4096 | Quantized older Qwen
| Qwen 3.8 27B FP8 | 32768 | 4096 | Biggest, best model.

The DTU group is added alongside OpenCode's available free models
and your other configured providers. This file does not restrict the provider
list or change your global configuration. Other providers may require their
own sign-in or API key.

**Does opening the folder start the models?** No. It connects to models that
Peter and Dimitrios have already started. If a model is unavailable, ask an
organiser.

See [OpenCode project configuration](https://opencode.ai/docs/config/#per-project).
</details>

### Free models from OpenCode
<details>
<summary>Model list</summary>

**Checked 22 September 2026, on OpenCode v2.** Every zero-priced model
OpenCode offers, as `opencode models` lists them. Free offers change without
notice: in one week DeepSeek V4 Flash Free dropped off the live list and MiMo
went from v2.5 to v2.6. Run `opencode models` if a name here does not match.

| Model, as the selector shows it | Model ID | Context |
|---|---|---:|
| Big Pickle | `opencode/big-pickle` | 200,000 |
| Ling 3.0 Flash Fin Free | `opencode/ling-3.0-flash-fin-free` | 262,144 |
| MiMo-V2.6-Flash Free | `opencode/mimo-v2.6-flash-free` | 200,000 |
| Nemotron 3 Ultra Free | `opencode/nemotron-3-ultra-free` | 1,000,000 |
| Nemotron 3.5 Lightning Free | `opencode/nemotron-3.5-lightning-free` | 262,144 |
| Muse Spark 1.2 Free ⚠️ | `opencode/muse-spark-1.2-contributor-free` | 1,048,576 |
| Muse Spark 1.3 Free ⚠️ | `opencode/muse-spark-1.3-contributor-free` | 1,048,576 |

All seven are priced at zero for input and output in the model catalogue.

**The two Muse Spark entries are contributor models.** A contributor model can
train on what you submit to it. The word `contributor` is in the model ID but
**not** in the name the selector shows you, which reads only "Muse Spark 1.2
Free". If you want to avoid them, check the ID rather than the name.

The five agents in exercise 2c run on the other five models for that reason.

Free does not mean private. The business model for a free LLM is your data and
your interaction with it. Use public exercise data with external models, and
send nothing confidential or personal. See
[OpenCode's model-specific privacy terms](https://opencode.ai/docs/zen/#privacy).

Sources: [live model list](https://opencode.ai/zen/v1/models),
[model catalogue](https://models.dev/api.json),
[Zen pricing](https://opencode.ai/docs/zen/#pricing).
</details>

### Jev, and why it is not in that table
<details>
<summary>A free model you will not find in the model selector</summary>

`jev-1.13-free` appears in OpenCode's live model list, so it is reasonable to
go looking for it. It will not be in your model selector, and `opencode models`
does not list it. That is not a bug.

**Jev is not a language model.** It is what TypeSafe AI call a *System One*
model, released 15 September 2026. It does not generate text. You give it a
state and a set of typed questions, and it returns values with probabilities:
yes/no, multiple choice, or a rubric score. The output is meant to be consumed
by your code as data, not read as prose.

It also uses a different endpoint, `https://opencode.ai/zen/v1/systemone`,
rather than the chat completions endpoint every model in the table above uses.
That is why OpenCode cannot offer it as a chat model, and why none of the
workshop exercises can run on it.

`jev-1.13` is priced at $0.042 per million input tokens with free output;
`jev-1.13-free` is free during a limited-time beta. TypeSafe AI claim up to
200x faster inference and 400x lower cost than comparable LLMs on
classification tasks. That is a vendor claim and we have not tested it.

Worth knowing about, because the shape of it is the interesting part: a
classifier with a typed interface is often the right tool for a decision you
are currently asking a chat model to make in prose and then parsing back out.
Not something you can select for these exercises.

Sources: [OpenCode Zen](https://opencode.ai/docs/zen/),
[live model list](https://opencode.ai/zen/v1/models).
</details>

### Show free models if they are hidden
<details>
<summary>Model management</summary>

- **Desktop:** open the model selector → **Manage models**, search for a
  model above, and turn its switch on under OpenCode. Return to the selector
  and choose it. Enable individual free models rather than every paid model.
- **Terminal:** type `/models`, search for the model name, and select it.
  It does not have to be a favourite to appear in search. If your version
  shows a Favourite action, you can use it for easier access next time.
- If the entire OpenCode provider is missing, check your other project/global
  configuration: remove only `"opencode"` from `disabled_providers`. If you
  intentionally use `enabled_providers`, include `"opencode"` alongside
  `"dtu"` and your other providers. The supplied workshop JSON sets neither
  restriction. Preserve unrelated settings; ask an organiser if unsure.
- Restart OpenCode after configuration changes. If a listed model is still
  absent, check your OpenCode version and the current live list; a setting
  cannot restore a retired offer. Do not add a paid model as a substitute
  unless you intend to pay.

The Desktop visibility switches and configuration restrictions are different
things. We do not change your saved visibility choices or global settings.
See [provider filtering](https://opencode.ai/docs/config/#disabled-providers).
</details>

### Your own subscriptions or API accounts
<details>
<summary>Other model selection</summary>

Use `/connect` in the terminal, or **Connect provider** in Desktop, choose
your provider, and complete its supported sign-in. Then select its model.
For example, OpenCode documents using a GitHub Copilot subscription.
Not every chat subscription includes third-party or API access; separate
API usage may be billed. Keep personal keys out of this repository.
See [supported providers and sign-in methods](https://opencode.ai/docs/providers/).

Changing the selected model changes the chat model. The supplied
`small_model: "dtu/gptoss"` still uses DTU GPT-OSS for background tasks;
there is no automatic fallback when DTU is offline. For an entirely external
setup, also change `small_model` in your own copy of `opencode.json` to your
chosen available provider/model ID.
</details>

## Exercises overview
We will introduce skills, agents and MCP as cornerstones of agentic processing through exercises.
* **Skills**: Reusable capabilities you or an AI agent can use to perform a task. For example, a “search web” skill, “read PDF” skill, or “send email” skill. Skills are like the **tools/actions** available to you/the agent.
* **Agents**: AI components that use skills to achieve a goal. An agent can **reason, plan, choose skills, execute actions, and adapt** based on the results.
* **MCP**: A standard way to connect the agent to a capability that lives outside OpenCode, such as a database or a public biological data service. The server is either a program OpenCode starts on your laptop, or a remote service it connects to over the network.

**Simple example:**
A travel-planning agent might have skills such as *search flights*, *find hotels*, and *create itinerary*. The **agent** decides which skills to use and in what order to plan the trip.

### Project folder design
This is the structure of the extracted folder. Everything you will be asked to
run or open is a path relative to this root, so the folder's own name does not
matter.
```text
AgenticWorkshop-main/
   opencode.json                Model connections, limits, permissions, MCP servers
   admin.md                     Server notes for the organisers
   .opencode/                   What OpenCode loads: agents and skills
      agents/
         bad-agent.md           Basic PDB agent example, Exercise 2a
         good-agent.md          More explicit PDB agent example, Exercise 2a
         genome-coordinator.md  Delegates to the four specialists below, Exercise 2c
         genome-auditor.md      Checks data, units and missing values
         genome-analyst.md      Writes and runs the analysis
         genome-visualizer.md   Makes the plots
         genome-reviewer.md     Independently rechecks the results
         submit-agent.md        Git-scoped agent, Exercise 4
      skills/
         skill-builder/         A subfolder INSIDE skills
            SKILL.md            The skill-builder instructions
         submit-work/           A second skill, Exercise 4
            SKILL.md            The submit-work instructions
   exercises/
      01-skills/
      02-agents/
         team-01/ ... team-10/  Your team's working folder for Exercise 2c
      03-mcp/
         data/                  The PDB snapshot, and byo/ for three other datasets
         scripts/               Rebuild the datasets and the DuckDB databases
      04-share/
         submissions/
            team-01/ ... team-10/   Where a team publishes its reviewed agents
   mcp/                         Notes on the four MCP servers this project configures
   slides/                      The concepts deck, published from Markdown
```
OpenCode reads `.opencode/` folder for project agents and skills, while `opencode.json` in the workshop root
contains the model connections, limits and permissions.

`skills` is the parent skill folder and `skill-builder` - the workshop supplied skill - is a separate subfolder
inside it. The complete path is `.opencode/skills/skill-builder/SKILL.md`.
GitHub collapses a chain of folders with a single child into one line, such
as `skills/skill-builder`; that is a compact display, not a single folder
name. With two skills present it no longer collapses `skills` itself.

Each additional skill gets its own subfolder and `SKILL.md`. Agent definitions
are Markdown files directly inside `.opencode/agents/`. A `.gitkeep` file in
an otherwise empty folder is only a Git/ZIP placeholder, not an agent or skill.

The `team-NN/` folders under `exercises/02-agents/` are working areas, not
loaded by OpenCode. Agents only take effect once you copy them into
`.opencode/agents/`. The matching folders under `exercises/04-share/submissions/`
are for publishing a reviewed copy, which is a separate step.

The leading dot may hide `.opencode` in your file browser, but OpenCode can
still read it. Do not rename it, move it out of the project, or put
`opencode.json` inside it. Open the repository root, not `.opencode` itself.

The `exercises/` and `mcp/` folders organize workshop materials. Creating
an `mcp/` folder does not activate an MCP server: `mcp/` holds documentation
only. An MCP server is configured under `mcp` in `opencode.json`, and is
either a program downloaded on demand or a remote service you connect to.
Four are configured and all ship switched off; Exercise 3 turns one on.
See [mcp/README.md](mcp/README.md) for what each provides.

See the OpenCode documentation for [agents](https://opencode.ai/docs/agents/)
and [skills](https://opencode.ai/docs/skills/).

### Exercises
- **Exercise 1** — [Skills](exercises/01-skills/README.md).
- **Exercise 2** — [Agents](exercises/02-agents/README.md).
- **Exercise 3** — [MCP and data analysis](exercises/03-mcp/README.md).
- **Exercise 4** — [Share what you built](exercises/04-share/README.md).
- **Bonus** — [Plugins, and finding bugs](exercises/05-bonus/README.md). Optional, any time.

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
<details>
<summary>Choose a task budget without consuming the whole shared service</summary>

Context is the space available for instructions, conversation, tool results
and the answer. Output is the maximum answer length, including reasoning.
Both are measured in tokens.

There are three different settings: the **server's verified maximum**, your
**selected context budget**, and your **answer limit**. Raising a number in
your JSON does not increase the server's capacity.

| Model | Student starting context | Student output |
|---|---:|---:|
| Qwen 3.6 | 16384 | 4096 |
| Qwen 3.8 | 32768 | 4096 |
| Mistral Nemo | 16384 | 4096 |
| GPT-OSS | 16384 | 4096 |

Start with the supplied values. If your task genuinely needs more, confirm
the available server limit with an organiser and then increase the budget.
**Above 32768 requires organiser approval while teams share the servers.**
**Do not select 262144 for ordinary workshop tasks.** Long requests consume
shared memory and processing time, leaving less capacity for other teams.
Setting a ceiling alone does not immediately allocate that entire amount.

These are useful sizes to recognise, not a requirement to use powers of two:

| Context value | When to consider it |
|---:|---|
| `4096` | Unsuitable with our `4096` answer allowance: input and instructions also need space |
| `8192` | Short tasks with enough room left for tools and input |
| `16384` | Default for GPT-OSS, Mistral and Qwen 3.6 |
| `32768` | Default for Qwen 3.8; confirm server support before increasing another model |
| `65536` | Only with organiser approval and a verified server capacity |
| `131072` | Target ceiling for Mistral/GPT-OSS; not a normal workshop budget |
| `262144` | Target ceiling for Qwen only; do not use without explicit approval |

### Change the budget in your own project

In `opencode.json`, find the model under `provider → dtu → models → model ID`.
Edit **only `limit.context`**, leaving `limit.output` at `4096`. For example,
after an organiser confirms Mistral can serve 32768:

```json
{
  "name": "Mistral Nemo 12B",
  "limit": {
    "context": 32768,
    "output": 4096
  }
}
```

This is one model entry, not a complete OpenCode configuration. Save the file and
restart OpenCode. Use plain integer digits: **`262144`, not `262.144` or
`262,144`**. Never exceed the model's verified server limit. The total includes
the answer; a 32768 context does not allow 32768 input tokens plus a 4096 answer.

This model entry applies to every agent using that provider/model ID in the
project. It is not an agent-level setting. Do not put `context` in an agent's
Markdown header or copy your personal configuration/keys into a team submission.
For a new experiment, use a fresh chat; compact or shorten an existing long
conversation before lowering its budget. Return to the supplied defaults
after your task.
</details>

## If something does not work
<details>
<summary>So many errors - so little time</summary>

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
</details>
---

For WorkShop organisers: [server administration and model settings](admin.md).
