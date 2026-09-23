---
marp: true
theme: dtu
paginate: true
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Building and employing agents

## For data analysis and visualization

Dimitrios S. Kanakoglou and Peter Wad Sackett
25 September 2026, DTU Health Tech

---

# Models and harnesses

The **model** generates text and proposes tool calls.
The **harness** runs the conversation and connects those calls to tools.

We use **OpenCode**. It reads your project, runs approved commands and
returns their results to the model so it can continue the task.

You can change the model while keeping the same harness and project.
The model server may be at DTU, but project commands run on your laptop.

<!-- Sources: https://opencode.ai/v2/docs/ and https://opencode.ai/v2/docs/providers/ -->

---

# Skills and agents

| | What you define | Example |
|---|---|---|
| **Skill** | Reusable instructions, with supporting scripts if needed | Download a PDB entry and check that it contains coordinates |
| **Agent** | A role, model and permissions, with instructions for doing its job | Review an analysis without editing its files |

OpenCode reads skills from `.opencode/skills/<name>/SKILL.md`
and agents from `.opencode/agents/<name>.md`.

An agent can load a relevant skill. A coordinator can delegate specific
jobs to other agents and combine their results.

<!-- Sources: https://opencode.ai/v2/docs/skills/ and https://opencode.ai/v2/docs/agents/ -->

---

# MCP (Model Context Protocol)

![width:1040](assets/mcp-overview.png)

[OpenCode MCP server documentation](https://opencode.ai/v2/docs/mcp-servers/)

<!-- Diagram supplied by Dimitrios. Examples illustrate the architecture, not a verified compatibility list. Configuration: https://opencode.ai/v2/docs/mcp-servers/ -->

---

# MCP servers and plugins

An **MCP server** exposes tools to the agent. In Exercise 3, a local
server lets the agent send SQL queries to DuckDB.

A **plugin** extends OpenCode itself. It can react to events or add
behaviour, such as a notification when work finishes.

Enable only the MCP servers you need. Inspect plugins before installing
them: they execute code, and their API must match your OpenCode version.

<!-- Sources: https://opencode.ai/v2/docs/mcp-servers/ and https://opencode.ai/v2/docs/plugins/ -->

---

# Free, paid and DTU models

| Choice | What you need to know |
|---|---|
| **OpenCode free models** | No model payment for the current free offers. Availability and limits can change. Requests leave DTU. |
| **Paid models** | Connect a supported subscription or API account. Check what it includes and how usage is billed. |
| **Four DTU models** | Workshop-hosted GPT-OSS, Mistral and two Qwens. Shared GPU capacity and context limits apply. |

Choose a model with `/models`. A chat subscription does not necessarily
include API access. We use public datasets throughout this workshop.

<!-- Sources: workshop README and opencode.json; https://opencode.ai/v2/docs/providers/ -->

---

# Three lessons before we start

1. **You are in charge of your data.** Check the provider and the
   permissions you approve. Use public data with external models.

2. **`/compact` is your friend.** Summarise a long conversation to make
   room. Keep important decisions in files because summaries lose detail.

3. **`/theme` helps you look cool in front of your PI.** Choose a theme
   you enjoy working with. Try it before starting the exercises.

<!-- Lessons from the workshop README. Compaction: https://opencode.ai/v2/docs/compaction/ -->

---

# HALp: the workshop helper

<pre style="position:absolute;right:64px;top:40px;font-size:22px;line-height:1.15;background:none;border:0;padding:0;"> [o_o]  &lt;{ let's look }
 /|_|\
  / \</pre>

Start a **fresh chat**, then type `/halp` and your question:

```text
/halp I am on Exercise 1c. Where should I copy my skill?
/halp Why can I not see the workshop agents?
```

HALp reads the exercise instructions and offers hints or setup help.
It can help with context settings, with your approval. It should leave
the exercise answers to you.

HALp initially uses a **free external model**. Share only public information
and redacted errors. Afterwards, select your exercise agent and model again.

---

# Exercise 1: skills

1. Open `exercises/01-skills/README.md` and follow **1a–1f**.
2. Discuss a PDB download skill in **Plan**, then create it in **Build**.
3. Retrieve an existing image, copy a skill and render coordinates.
4. Use `skill-builder` to improve a skill, then make one of your own.

**Tips**

- Specify the input, output folder and what should happen on failure.
- Test another valid input and an invalid one. Inspect the saved files.

---

# Exercise 2a–2b: agents

1. Open `exercises/02-agents/README.md`.
2. Give `bad-agent` and `good-agent` the same PDB 4HHB request in
   separate chats, using the same model.
3. Open both outputs and compare them.
4. Create and test your own agent in `.opencode/agents/`.

**Tips**

- Give your agent one clear job, expected outputs and permission rules.
- Check that the viewer loads and its controls work before adding features.

---

# Exercise 2c: a team of agents

1. Select `genome-coordinator` and use the invocation prompt in **2c**.
2. Follow the auditor, analyst, visualizer and reviewer as they work.
3. Open the report, plots and review. Check the reported model IDs.
4. Choose a different question and build your own coordinator and specialists.

**Tips**

- Give each specialist explicit input paths and a specific output to produce.
- Check child-agent approval requests. A waiting approval can pause the team.

---

# Exercise 3: MCP and data analysis

1. Open `exercises/03-mcp/README.md` and build the supplied DuckDB database.
2. Use `/mcps` to enable **duckdb**. Leave the other servers off initially.
3. Follow the questions and checks in **3a–3g**.
4. For **3h**, choose a supplied alternative dataset or your own public data.

**Tips**

- Ask for the SQL, row counts and missing-value handling with each answer.
- Check a small result independently before trusting the full analysis.

---

# Exercise 4: sharing

1. Open `exercises/04-share/README.md`.
2. Put reviewed files in your team's submission folder.
3. Ask `submit-agent` to inspect them with `submit-work` before publishing.
4. Submit through your fork and a pull request, then try another team's work.

**Tips**

- Include supporting scripts and skills. Remove credentials and private data.
- A ZIP cannot push changes. Use a Git clone or the GitHub upload interface.

---

# Bonus: plugins and debugging

1. Open `exercises/05-bonus/README.md`.
2. Inspect the example plugin and test its compatibility with your version.
3. Review the supplied BED analysis, then build checks with known answers.
4. Keep the original script and compare it with your corrected copy.

**Tips**

- Read plugin code before installing it. Check the log if it does not load.
- `/fork` branches the conversation. Preserve files separately before edits.
