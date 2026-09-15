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

## Quick start — download, extract and open

1. Install [OpenCode](https://opencode.ai/docs/#install) before the workshop.
   For this workshop, Windows users should install and run it inside WSL2.
   The terminal version is preferred; OpenCode Desktop is also supported.
2. For Linux and WSL2 Ubunbu (Linux) it is this command for install OpenCode CLI (terminal)<br>
   `curl -fsSL https://opencode.ai/install | bash` 
3. Open [the workshop repository](https://github.com/peterwadsackett/AgenticWorkshop)
   and choose **Code → Download ZIP**.
4. Extract the ZIP and move/rename the extracted folder to the place you want to work.
   Its default name is `AgenticWorkshop-main` and we suggest renaming it to `workshop`
   in your home, and we will refer to that name in the text.
6. In **OpenCode Desktop**, open that extracted folder as your project—the
   folder containing both `README.md` and `opencode.json`, not its parent.
   For the terminal version, run `opencode` from inside that folder.
7. Start a new chat. Open the model selector and choose a model under **DTU**.
   In the terminal version, type `/models`.

**For the supplied DTU models, no JSON editing, manual merging, API key or
Custom provider setup is needed.**
Leave your existing global `opencode.jsonc`, `package.json` and
`node_modules` alone. OpenCode combines the project configuration with your
global settings automatically.

## LLM Models you can use
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
   
**Checked 15 September 2026.** The table includes all non-deprecated, zero-priced
models present in both OpenCode's live model list and its model catalogue at the
time of checking. Free offers can change or disappear; listing is not a
guarantee that a request will succeed.<br>
Be aware that the business model for free LLM models is to train on your data and your interaction with the model.

| Model | OpenCode model ID | Listing |
|---|---|---|
| Big Pickle | `opencode/big-pickle` | Free in Zen pricing |
| MiMo-V2.5 Free | `opencode/mimo-v2.5-free` | Free in Zen pricing |
| Ling 3.0 Flash Fin Free | `opencode/ling-3.0-flash-fin-free` | Free in Zen pricing |
| Nemotron 3 Ultra Free | `opencode/nemotron-3-ultra-free` | Free in Zen pricing |
| Nemotron 3.5 Lightning Free | `opencode/nemotron-3.5-lightning-free` | Free in Zen pricing |
| Muse Spark 1.3 Contributor Free | `opencode/muse-spark-1.3-contributor-free` | Free in Zen pricing |
| Muse Spark 1.2 Contributor Free | `opencode/muse-spark-1.2-contributor-free` | Live list + zero-priced catalogue entry |

Sources: [OpenCode Zen pricing](https://opencode.ai/docs/zen/#pricing),
[live model list](https://opencode.ai/zen/v1/models), and
[model catalogue](https://models.dev/api.json). Muse Spark 1.2 is not in the
current Zen pricing table; check its displayed price and terms before use.
Deprecated offers are excluded even if an old endpoint still lists them.

Use public exercise data with external models. Free offers can allow data
collection or model improvement; Contributor models can include training
on submitted content. Do not send confidential or personal data.
See [OpenCode's model-specific privacy terms](https://opencode.ai/docs/zen/#privacy).
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
We will introduce skills and agents as cornerstones of agentic processing through exercises.
* **Skills**: Reusable capabilities you or an AI agent can use to perform a task. For example, a “search web” skill, “read PDF” skill, or “send email” skill. Skills are like the **tools/actions** available to you/the agent.
* **Agents**: AI components that use skills to achieve a goal. An agent can **reason, plan, choose skills, execute actions, and adapt** based on the results.

**Simple example:**
A travel-planning agent might have skills such as *search flights*, *find hotels*, and *create itinerary*. The **agent** decides which skills to use and in what order to plan the trip.

### Project folder (workshop) design
The downloaded and extracted workshop has this structure.
```text
workshop/
   opencode.json                Model connections, limits and permissions
   .opencode/
      agents/
         bad-agent.md           Basic PDB agent example
         good-agent.md          More explicit PDB agent example
      skills/
         skill-builder/         A subfolder INSIDE skills
         SKILL.md               The skill-builder instructions
   exercises/
      01-skills/
      02-agents/
   mcp/                         Reserved for MCP-related materials
```
OpenCode reads `.opencode/` folder for project agents and skills, while `opencode.json` in the workshop root
contains the model connections, limits and permissions.

`skills` is the parent skill folder and `skill-builder` - the workshop supplied skill - is a separate subfolder
inside it. The complete path is `.opencode/skills/skill-builder/SKILL.md`.
GitHub may display `skills/skill-builder` together when it is the only
subfolder; that is a compact display, not a single folder name.

Each additional skill gets its own subfolder and `SKILL.md`. Agent definitions
are Markdown files directly inside `.opencode/agents/`. A `.gitkeep` file in
an otherwise empty folder is only a Git/ZIP placeholder, not an agent or skill.

The leading dot may hide `.opencode` in your file browser, but OpenCode can
still read it. Do not rename it, move it out of the project, or put
`opencode.json` inside it. Open the repository root, not `.opencode` itself.

The `exercises/` and `mcp/` folders organize workshop materials. Creating
an `mcp/` folder does not activate an MCP server.

See the OpenCode documentation for [agents](https://opencode.ai/docs/agents/)
and [skills](https://opencode.ai/docs/skills/).

### Exercises
- **Exercise 1** — [Skills](exercises/01-skills/README.md).
- **Exercise 2** — [Agents](exercises/02-agents/README.md).
- **Exercise 3** — [Data processing](exercises/02-agents/README.md).

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
