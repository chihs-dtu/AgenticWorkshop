---
marp: true
theme: dtu
paginate: true
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Welcome to the Agentic Workshop

## This workshop is hands on

Dimitrios S. Kanakoglou and Peter Wad Sackett · 25 September 2026

---

## The harness

We start with the harness, because that is what you install and what you sit
in front of all day.

Ours is **OpenCode**. There are plenty of others: Claude Code, Codex CLI,
Cursor, Aider, Gemini CLI, Pi. We use OpenCode because it is modular and
model-agnostic, which makes it suitable for scientific use: you choose the
model, and the data goes where you decide.

**Version 2 went live on 22 September 2026.** These materials are written for
v2.

---

## Five things, and what each one is

**Agent** — an autonomous program powered by an LLM that can perceive its
environment, reason through multi-step plans, and execute actions toward an
objective.

**Skill** — a packaged set of workflow instructions, usually a `SKILL.md`,
that teaches an agent a specific repeatable task, loaded when relevant.

**MCP** — an open protocol, a USB-C port for AI, connecting an agent to
external data sources and tool backends.

**Harness** — the runtime, guardrails and execution environment that make an
agent reliable, safe and auditable.

**Plugin** — one installable package that bundles agents, skills, MCP servers
and hooks into a portable unit.

---

## Install

The CLI version. Instructions are in the repository README.

```bash
npm install -g @opencode/cli
opencode --version
```

Open the extracted folder, the one containing `opencode.json`.

The DTU models come from the project configuration and load a few seconds
after the rest.

---

<!-- _class: part -->

# Exercise 1

## Skills

---

## Skills

Turn a task you repeat into instructions an agent can load.

You will build a skill through conversation, test it, and improve it from what
broke. Then use `skill-builder`, which is a skill for making skills.

A skill is Markdown. It advises; it does not execute.

<span class="note">exercises/01-skills</span>

---

<!-- _class: part -->

# Exercise 2

## Agents

---

## Agents

Two supplied agents get the same request. One is vague, one is explicit.
You compare the output, then write your own.

An agent is a role plus permissions. The same model runs all of them.

**2c** is a team: one coordinator and four specialists, each on a different
model, all free.

<span class="note">exercises/02-agents</span>

---

<!-- _class: part -->

# Exercise 3

## MCP and data analysis

---

## MCP

An agent connected to a DuckDB database of 259,693 PDB entries. You ask in
English, it writes SQL.

`/mcps` turns a server on for the session. Four are configured and all ship
switched off.

Three more datasets are supplied if you want something that is not the PDB.

<span class="note">exercises/03-mcp</span>

---

<!-- _class: part -->

# Exercise 4

## Share what you built

---

## Sharing

Publish your skill or agent as a pull request, from a fork.

The checks before publishing are part of the exercise: what is in the diff,
whether anything is being silently ignored, whether there are secrets.

<span class="note">exercises/04-share</span>

---

<!-- _class: part -->

# Bonus

## Optional, any time

---

## Bonus exercises

**5a Plugins.** What they are, what to check before installing one, and why a
plugin is a different risk from a skill.

**5b Finding bugs.** A script that runs, exits cleanly, and prints three
numbers that are wrong. Five steps, starting with what OpenCode already has.

<span class="note">exercises/05-bonus</span>

---

<!-- _class: lead -->

# Thank you

<span class="note">github.com/peterwadsackett/AgenticWorkshop</span>
