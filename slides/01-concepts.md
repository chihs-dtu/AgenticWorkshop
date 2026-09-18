---
marp: true
theme: dtu
paginate: true
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Building and employing agents for data analysis

## Skills, agents and MCP

Dimitrios S. Kanakoglou and Peter Wad Sackett

<!--
Presenter notes live in HTML comments. GitHub hides them when it renders this
file as a document; Marp shows them in presenter view (press P).
-->

---

## Where we are going

| | Exercise | The thing you build | The thing you learn |
|---|---|---|---|
| **1** | Skills | A `pdb-download` skill | A successful HTTP request is not a structure file |
| **2** | Agents | Your own agent | An agent claiming success is not success |
| **3** | MCP | A DuckDB server over 259,693 PDB entries | A query that runs is not an answer that is true |
| **4** | Share | A pull request | "Committed" is not "in the repository" |

Four different tools. **One habit**: check the thing itself, not the report about it.

---

<!-- _class: part -->

# Part 1
## Three words that are not synonyms

---

## Start from what a model actually is

A language model takes text and produces text. That is the whole of it.

It cannot read your disk, run a command, or fetch a file. Everything that
*feels* agentic is scaffolding **around** the model:

- something that **tells it what to do** → a **skill**
- something that **decides what to do and what it may touch** → an **agent**
- something that **connects it to the outside world** → an **MCP server**

<span class="note">Three different problems. They are not interchangeable, and the
common mistake is reaching for the newest of them.</span>

---

## Skill — reusable instructions

A folder with a `SKILL.md`: YAML header (`name`, `description`) plus Markdown.

```text
<project>/.opencode/skills/<skill-name>/SKILL.md   ← this project only
~/.config/opencode/skills/<skill-name>/SKILL.md    ← all your projects
```

- It is **prose**, loaded on demand when the description matches the task.
- It **executes nothing**. Scripts shipped alongside it do the work.
- Supporting files travel with the folder — copying only `SKILL.md` can
  leave a skill that half-exists.

> A skill is guidance. It says *what a trustworthy answer has to contain*.

---

## Agent — a role with permissions

A single Markdown file: YAML frontmatter for settings, body for instructions.

```markdown
---
description: Checks a supplied analysis and reports evidence-backed findings
mode: primary
steps: 20
permission: { edit: ask, bash: ask, task: deny }
---
Inspect the supplied files and identify the question the analysis addresses...
```

- **Not a new model.** The same model runs every agent you write.
- What changes is the **instructions**, the **permissions**, and the **step budget**.
- `bad-agent` and `good-agent` in Exercise 2 differ only in their prose.

---

## MCP — a connection to something outside

Model Context Protocol: a standard way for OpenCode to talk to a capability
that is not part of it.

```json
{ "type": "local",  "command": ["uvx", "mcp-server-motherduck@1.0.8"] }
{ "type": "remote", "url": "https://mcp.platform.opentargets.org/mcp" }
```

- **Local** — a child process on your laptop, stdin/stdout, no network port.
  Your data stays put. Costs a one-time download and needs `uv`.
- **Remote** — someone else's server over HTTPS. Nothing to install; your
  queries leave your machine and their downtime is your downtime.

---

<!-- _class: tight -->

## The one slide to remember

| | **Skill** | **Agent** | **MCP server** |
|---|---|---|---|
| Is | Instructions | A role + permissions | A capability |
| Answers | *How should this be done?* | *Who decides, and what may they touch?* | *What can be reached at all?* |
| Lives in | `.opencode/skills/<name>/SKILL.md` | `.opencode/agents/<name>.md` | `mcp` block in `opencode.json` |
| Costs | Tokens only when loaded | Nothing extra | **Every tool described in every request** |
| Executes code | No | No — it permits | Yes |
| You get it wrong by | Growing one skill to cover everything | Hardcoding a model into it | Adding one because it exists |

---

## The decision, with a real answer

*"I want an assistant that is good at git. Which of the three?"*

| | What it gives | Verdict |
|---|---|---|
| **MCP server** | `mcp-server-git`, 12 tools: `git_status`, `git_diff`, `git_commit`… | **No.** 1,588 tokens — 10% of a DTU context — in *every* request, and it has **no push, no remote, no pull-request tool.** For an exercise about publishing, it cannot do the one required thing. |
| **Skill** | What to check before publishing, what never to commit | **Yes.** `git` already works through `bash`. The missing piece was knowledge, not capability. |
| **Agent** | Inspect freely, ask before publishing, refuse force-push | **Useful.** |

<span class="note">Measured, not guessed — Exercise 4a.</span>

---

<!-- _class: part -->

# Part 2
## Why modular

---

## Because you can replace one piece without touching the others

Exercise 3 hands a DuckDB MCP server a PDB snapshot. Exercise 3h points it
at **your** data:

```json
"--db-path", "my_data.duckdb",
```

One argument. The server, its four tools, the agent, the skill and every
permission rule are unchanged — **because a DuckDB server is not a PDB tool.**
It is a SQL tool that Exercise 3 happened to hand a PDB database.

> When you consider adopting anything, ask what it is actually coupled to.

---

## Guidance and capability are separate, and you need both

Exercise 3e: the checks you were doing by hand become a skill.

- The **MCP server** runs the SQL. *(capability)*
- The **skill** says an answer must state the SQL, the row count, and which
  experiment types it covers. *(guidance)*
- The **agent** says the query needs your approval before it runs. *(authority)*

The skill executes nothing. The server knows nothing about NMR. The agent
writes no SQL.

**Three separable concerns. Monolithic tools make you rebuild all three
whenever one changes.**

---

<!-- _class: part -->

# Part 3
## Why OpenCode

---

<!-- _class: tight -->

## What we actually needed from a tool

| Requirement | Why it mattered for this workshop |
|---|---|
| **Provider-agnostic** | 4 DTU models on our cluster, through one `opencode.json` block — no vendor account required to attend |
| **Config in the repository** | You download a ZIP and everything is configured. No per-laptop setup |
| **Open source (MIT)** | We can read what it does with your files and your keys |
| **Permissions built in** | `allow` / `ask` / `deny` per tool, per command pattern — Exercise 2 is *about* this |
| **Skills, agents and MCP in one tool** | The three concepts are separable *in the same program*, so you can compare them |
| **Terminal-first** | Works on a laptop, over SSH, inside WSL2, in a lecture room with bad wifi |

<span class="note">208k stars, MIT — checked 18 September 2026.</span>

---

## It is not the only one — meet `oh-my-pi`

`can1357/oh-my-pi` (OMP) — *"Coding agent with the IDE wired in"*. MIT,
TypeScript + ~80k lines of Rust core on Bun. **31.8k stars.**

What it adds that a plain agent does not have:

- **LSP wired into every write** — real rename-refactoring across re-exports
  and barrel files, not regex-and-hope
- **DAP** — it drives `lldb`, `dlv`, `debugpy`: sets breakpoints, steps,
  reads stack frames on a crash
- Persistent Python/JS sessions, structural editing, browser automation

<span class="note">Different bet on the same problem: OpenCode is more polished for ordinary
code; OMP has the deeper machinery. Worth knowing it exists before you conclude
"agents can't debug".</span>

---

## The ecosystem, and its shape

`awesome-opencode` — 10.3k stars — lists plugins, themes, agents, projects
and resources. Over 100 community plugins alone:

<div class="cols">

- Parallel background task execution
- Persistent agent memory blocks
- Multi-agent workflow orchestration
- Context compression (claims 60–90% fewer tokens)
- Task-specific agent teams
- Automatic session naming

</div>

**Nothing here is reviewed by anyone.** Hold that thought until Part 6.

---

<!-- _class: part -->

# Part 4
## The context window is the budget

---

## Every tool is described in every request

You are not paying for what a server *does*. You are paying for its **tool
list**, on every single message, whether you use it or not.

| Server | Tools | Tool definitions | Share of a 16,384-token DTU context |
|---|---:|---:|---:|
| `duckdb` | 4 | ~780 | 5% |
| `opentargets` | 5 | ~4,400 | 27% |
| `biomcp` | 83 | ~17,400 | **106%** |
| `rcsb` | 38 | ~21,200 | **129%** |

BioMCP covers 43 biomedical databases and is excellent. **Its tool list does
not fit in a DTU model's context before anyone asks anything.**

---

## So: tool count, not features, is the limit

Two consequences you will feel on the day:

1. **Turn off servers you are not using.** An idle server is a permanent tax
   on the conversation, not a dormant option.
2. **Breadth costs accuracy too.** A small model picks the wrong tool far
   more often when choosing among 83 than among 4.

`rcsb` is narrow and deep (38 structural tools). `biomcp` is wide and shallow
(one tool per resource, 43 databases). **Neither fits a 16k model.** Use the
large-context models for those, or don't connect them.

---

<!-- _class: part -->

# Part 5
## Local models, frontier models

---

<!-- _class: tight -->

## When to use which

| | **Local / on-prem** (our DTU models) | **Frontier** (Claude, GPT, Gemini) |
|---|---|---|
| **Patient or unpublished data** | **Yes.** Nothing leaves the cluster | No, unless you have a data-processing agreement |
| **Cost per token** | Fixed: the GPU is already bought | Per-call, and agentic loops multiply it |
| **Context** | 16k–32k here — the real constraint | 200k–1M, so tool lists stop mattering |
| **Long multi-step tasks** | Struggles — loses the thread | Where the gap is widest |
| **Offline / air-gapped** | Works | Does not exist |
| **Reproducibility for a paper** | You can pin the weights | The endpoint changes under you |

---

## Rule of thumb

**Local first when the data is sensitive, the task is narrow, or the loop is
long and cheap to retry.**
Downloading a file. Renaming columns. Summarising a log. Drafting a skill.
One well-described tool call.

**Frontier when the task is genuinely hard and the data is public.**
Debugging why an analysis is wrong. Reading a repository you have never seen.
Composing a query against a schema it has just been handed.

**Never either one when the answer matters and you have not checked it.**
That applies identically to both — which is Part 6.

---

## What "frontier" does and does not buy you

**BixBench** — 53 real bioinformatics scenarios, ~300 open-answer questions.
Agents get an empty notebook, the data files, and the questions.

### Frontier models scored 17%

> *"…frontier models only achieve 17% accuracy in the open-answer regime, and
> no better than random in a multiple-choice setting."*

That is on tasks your PhD students do. The gap between a 16k local model and
a frontier model is real, but **neither is anywhere near "trust the output".**

<span class="note">Mitchener et al., arXiv:2503.00096 — evaluating GPT-4o and Claude 3.5 Sonnet.</span>

---

<!-- _class: part -->

# Part 6
## The habit the whole workshop is built on

---

<!-- _class: tight -->

## Four claims that sound the same and are not

| You are told | It means | It does **not** mean |
|---|---|---|
| HTTP 200 | A response arrived | The file is a structure and not an error page |
| `✓ duckdb connected` | A process started and answered a handshake | The database file exists — it is opened on first query |
| The SQL ran, no error | The syntax was valid | The question was answerable as asked |
| "Committed successfully" | The agent ran `git commit` | Your files are in the repository — `.gitignore` is silent |

**Each is one command away from being checked.** That command is the exercise.

---

## The example worth remembering

> *"What is the average resolution of structures in the PDB?"*

```sql
SELECT avg(resolution) FROM entries;     -- 2.362 Å
```

Valid SQL. Plausible number. A crystallographer would not blink. **And it
silently excluded 15,104 entries**, because `avg()` skips NULLs:

```sql
SELECT count(*), count(resolution) FROM entries;   -- 259,693 | 244,589
```

Group the blanks by method: **every SOLUTION NMR entry, and only those.**
NMR structures have no resolution — the concept does not apply.

---

## Why no model was going to catch that

The agent did nothing wrong. The SQL was correct. The number was real.

**The question was unanswerable as asked, and nothing in the output said so.**

Knowing that "average resolution of the PDB" needs qualifying is **domain
knowledge** — yours, not something recoverable from a schema. The check that
exposed it took one query: compare `count(*)` with `count(column)`.

> This is the job that does not get automated. Everything else is typing.

---

## Permissions are tool controls, not a sandbox

Two failures of the same shape, from two different exercises:

- `edit: deny` does **not** make an agent read-only if `bash` can still write
  files.
- DuckDB in read-only mode refuses `CREATE`, `UPDATE`, `DELETE`, `ATTACH` —
  and then this succeeds:

```sql
COPY (SELECT 1 AS x) TO 'PROOF.parquet' (FORMAT parquet)
```

A read-only **database** is not a read-only **filesystem**. `read_csv()` will
open anything the process can reach.

**A safety property is only as broad as the mechanism enforcing it.**
Keep approval prompts on. Do not test an `ask` rule in auto-approve mode.

---

<!-- _class: part -->

# Part 7
## Before you install anything from the internet

---

<!-- _class: warn -->

# Read this before you download a single skill

A `SKILL.md` is **instructions your agent will follow.**
An agent file is **a permission policy you are adopting.**
An MCP entry is **a program you are about to run on your laptop.**

None of them look like code. All three are code's equal in what they can do.

> Treat a downloaded skill the way this workshop tells you to treat downloaded
> data: **material to inspect, not instructions to obey on sight.**

<span class="note">Exercise 4d says exactly this, and it is the one instruction in the
workshop with a real adversary behind it.</span>

---

<!-- _class: warn -->

## This is not a hypothetical

**`@bitwarden/cli` 2026.4.0** — a compromised release of a *password manager's*
CLI, April 2026. A `preinstall` hook, running before any test or check, pulled
down a 10 MB obfuscated payload. It harvested:

- SSH private keys · AWS, GCP and Azure credentials · npm tokens
- Git credentials · environment variables · shell history
- **Claude Code auth tokens, and MCP server configs — which contain API keys
  and database credentials**

Then it published the loot to a public GitHub repository **under the victim's
own account**, and left the token there for the next infected machine to reuse.

<span class="note">Aikido Security, 23 April 2026. Part of the Shai-Hulud family.</span>

---

<!-- _class: warn -->

## The same campaign, at scale

| Wave | When | Reach |
|---|---|---|
| Shai-Hulud | Sept 2025 | Maintainer phishing → widely used npm packages |
| Shai-Hulud 2.0 | Nov–Dec 2025 | 700+ npm packages; 27,000+ malicious GitHub repos |
| "Mini" expansion | May 2026 | 170+ npm and 2 PyPI packages, 404 malicious versions |

That May 2026 variant installed persistence as a **`.claude/settings.json`
SessionStart hook** — it lives in your agent's configuration and runs every
time you open a session.

**Your AI tooling is not a bystander in these attacks. It is the target.**

<span class="note">Microsoft Security, 9 Dec 2025; Zscaler; CSA Singapore AD-2026-009.</span>

---

<!-- _class: warn -->

## And the agent itself can be turned against you

**MCP Tool Poisoning** (OWASP):

> *"…an indirect prompt injection attack targeting AI agents that connect to
> external tool servers via the Model Context Protocol."*

Tool **descriptions** get reviewed when you connect. Tool **responses** flow
straight into the model's context with no equivalent check. A malicious server
returns hidden instructions inside a normal-looking result — and the model
treats them as trusted input.

<span class="note">In April 2026, researchers hijacked Claude Code, Gemini CLI and GitHub
Copilot by putting instructions in GitHub **pull-request titles**, and got them to
exfiltrate Actions secrets.</span>

---

<!-- _class: warn -->

## Before you install anything: five questions

1. **Read the `SKILL.md` or agent file yourself.** It is prose. It takes two
   minutes. Ask your agent to summarise what it instructs and what it touches
   — *in Plan mode, before it can act.*
2. **Does the install run code?** `curl … | bash` and `npm install -g` both
   execute on your machine before you have read anything.
3. **Who wrote it, and who has reviewed it?** 21 stars means nobody has.
4. **What credentials can the process reach?** SSH keys, cloud config, your
   `opencode.json` — all readable by anything you run as you.
5. **Does the package name actually exist, or did a model invent it?**

**Approval prompts are not friction. They are the only checkpoint you have.**

---

## The last one has a name: slopsquatting

Models invent package names. Attackers register the invented names.

| Study | Models | Hallucinated package references |
|---|---|---:|
| Spracklen et al., USENIX Sec '25 | commercial | **5.2%** |
| " | open-source | **21.7%** |
| Churilov, arXiv 2026 | 2026 frontier cohort | **4.62–6.10%** |

205,474 unique fabricated package names across 576,000 generated samples.

**The spread narrowed; the floor did not go away.** A local model is more
likely to invent a dependency than a frontier one — one more input to the
local-vs-frontier decision, and a reason to read `pip install` lines.

---

<!-- _class: part -->

# Part 8
## Where to go after today

---

<!-- _class: tight -->

## Four worth reading — *reading*, not installing

| Repository | What it is | Why look |
|---|---|---|
| **[awesome-opencode](https://github.com/awesome-opencode/awesome-opencode#plugins)**<br>★10.3k | Curated plugins, themes, agents and projects | The map of what people are building |
| **[can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)**<br>★31.8k · MIT | Coding agent with LSP + DAP wired in | A different answer to the same question |
| **[darrenhinde/OpenAgentsControl](https://github.com/darrenhinde/OpenAgentsControl)**<br>★4.9k · MIT | Plan-first agents, approval-gated execution, for OpenCode | Multi-agent structure done deliberately |
| **[amrahman90/python-expert-agent](https://github.com/amrahman90/python-expert-agent)**<br>★21 · MIT | 10 skills + 4 subagents for Python | A realistic small repo — read every line |

<span class="note">Both bottom entries install by executing a script (`curl … \| bash`, `npm install -g`).
Star counts checked 18 September 2026 and they are not a safety rating: the 4.9k one
and the 21-star one carry the same risk if you run the installer unread.</span>

---

## And one paper, for the bioinformaticians

### Paper2Agent — *Nature*, 16 September 2026

Miao, Davis, Zhang, Pritchard & Zou turn a published paper — manuscript, code
and data — into **an MCP-based agent**: a "virtual corresponding author" that
reproduces the paper's results, applies its methods to your data, and answers
questions about it.

They then had several paper-agents **collaborate**, and prioritised a causal
gene for psoriasis.

**This is the same three-part architecture you are learning today**, pointed at
the reproducibility problem. It is two days old. You are not late.

---

<!-- _class: refs -->

## References — workshop claims

1. **Protein Data Bank.** Berman HM *et al.* (2000) *Nucleic Acids Research* **28**:235–242. doi:10.1093/nar/28.1.235
2. **The resolution revolution.** Kühlbrandt W (2014) *Science* **343**:1443–1444. doi:10.1126/science.1251652 — *the cryo-EM trend you reproduce in Exercise 3d.*
3. **AlphaFold.** Jumper J *et al.* (2021) *Nature* **596**:583–589. doi:10.1038/s41586-021-03819-2
4. **Paper2Agent: Reimagining research papers as interactive and reliable AI agents.** Miao J, Davis JR, Zhang Y, Pritchard JK, Zou J (2026) *Nature*, advance online 16 Sept 2026. doi:10.1038/s41586-026-11044-y
5. **BixBench: a Comprehensive Benchmark for LLM-based Agents in Computational Biology.** Mitchener L *et al.* (2025) arXiv:2503.00096
6. OpenCode documentation — [skills](https://opencode.ai/docs/skills/) · [agents](https://opencode.ai/docs/agents/) · [permissions](https://opencode.ai/docs/permissions/) · [MCP](https://opencode.ai/docs/mcp-servers/)

---

<!-- _class: refs -->

## References — security claims

7. **We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs.** Spracklen J, Wijewickrama R, Sakib AHMN, Maiti A, Viswanath B, Jadliwala M (2025) *34th USENIX Security Symposium*. arXiv:2406.10279
8. **The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort.** Churilov A (2026) arXiv:2605.17062
9. **MCP Tool Poisoning.** OWASP Community. https://owasp.org/www-community/attacks/MCP_Tool_Poisoning
10. **Shai-Hulud 2.0: guidance for detecting, investigating, and defending against the supply chain attack.** Microsoft Security Blog, 9 December 2025
11. **Compromised Bitwarden CLI contains a self-propagating npm worm.** Aikido Security, 23 April 2026
12. **Ongoing npm supply chain attack (Shai-Hulud worm).** Cyber Security Agency of Singapore, advisory AD-2026-009

<span class="note">Repository metadata, star counts and tool-token measurements checked 18 September 2026.</span>

---

# Three things to take away

1. **A skill is instructions. An agent is authority. A server is capability.**
   Ask which one the job needs before you reach for the newest.

2. **Tool count, not features, is what a small model can afford.**
   Every tool is described in every request, used or not.

3. **Nothing an agent tells you counts until you have checked the thing itself.**
   A 200, a handshake, a clean query and a commit are all claims, not results.

### github.com/peterwadsackett/AgenticWorkshop
