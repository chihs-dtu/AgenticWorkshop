# Exercise 4 — Share what you built

The short one. You have made a skill, an agent, or an MCP configuration.
Publish it to the workshop repository so the rest of the room can use it.

The point is not git. The point is that **publishing is the first thing you
have done in this workshop that other people can see, and that you cannot
quietly undo.** Everything before this was a file on your laptop.

You need a GitHub account, and `gh` installed and signed in:

```bash
gh auth status
```

If that fails, run `gh auth login` first, or pair with someone who is signed
in. Ask an organiser if you would rather not create an account — you can hand
your folder over directly instead.

---

# Exercise 4a — Decide first: skill, agent, or MCP server?

Before doing the task, answer the question the task raises. You want an
assistant that is good at git. Which of the three does that?

Start in **Plan** mode and ask:

> I want to publish my own skill to a shared GitHub repository as a pull
> request. Should that be an MCP server, a skill, or an agent? Compare them
> for this specific job.

Then check the answer against this, which was measured rather than guessed:

| | What it would give you | Verdict for this job |
|---|---|---|
| **MCP server** | `mcp-server-git` is maintained and exposes 12 tools: `git_status`, `git_diff`, `git_commit`, `git_add`, `git_log`, `git_checkout`, … | **No.** It costs 1,588 tokens — 10% of a DTU model's context — in every request, and it has **no push, no remote and no pull-request tools**. For an exercise about publishing, it cannot do the one thing required. You would still fall back to `bash`. |
| **Skill** | Guidance: what to check before publishing, what never to commit, which commands in which order | **Yes.** `git` and `gh` already work through `bash`. What is missing is not capability, it is knowing what to check. |
| **Agent** | Permissions: which commands run freely, which need approval, which are refused outright | **Useful.** Inspecting is free; publishing asks; history rewriting is blocked. |

This is Exercise 3g's question with a concrete answer. `bash` already covers
git, so the MCP server adds context cost and removes nothing from your plate.
**"There is an MCP server for it" is not a reason to connect one.**

The workshop supplies both of the useful ones:

- [`submit-work`](../../.opencode/skills/submit-work/SKILL.md) — the skill
- [`submit-agent`](../../.opencode/agents/submit-agent.md) — the agent

---

# Exercise 4b — Look at what you are about to make public

Copy what you are sharing into `submissions/<your-name>/`, then, **in Plan
mode**, with `submit-agent` selected:

> Use the submit-work skill. I want to share the skill I built in Exercise 1.
> Show me exactly what would be published and what your checks found. Do not
> commit or push anything yet.

Reading `git status`, `git diff` and `git check-ignore` needs no approval, so
the agent can inspect freely. It should report five things: what would be
committed, that nothing is silently ignored, that there are no credentials,
that there are no large or generated files, and that the submission is
self-contained.

## The check that catches the real mistake

The repository's `.gitignore` is the standard Python one. It excludes these
names **anywhere** in the tree:

```text
build   dist   lib   var   target   venv   env   downloads   sdist   wheels   eggs
```

Name your folder `build` and your submission vanishes. No error, no warning,
`git status` shows nothing to commit, and you find out when your pull request
is empty. This is not hypothetical — Exercise 3's scripts were originally in
a folder called `build/` and were silently dropped from the published ZIP.
They are in `scripts/` now because of it.

```bash
git check-ignore -v exercises/04-share/submissions/your-name/*
```

No output is the passing result.

**What to notice:** the agent reporting "committed successfully" and the
files actually being in the repository are different claims. Same lesson as
"a successful HTTP request is not a structure file" in Exercise 1, and "a
query that succeeded is not a correct answer" in Exercise 3. Check the thing
itself.

---

# Exercise 4c — Publish it

Switch to **Build** and let it proceed. You will be asked to approve three
things, because each one is public and hard to reverse: the fork, the push,
and the pull request.

Read each request before approving. The agent refuses force pushes, hard
resets and rebases outright — those are the ones that damage other people's
copies, not just your own.

When it finishes you get a pull request URL. Open it and check the **Files
changed** tab yourself. That tab is the truth; the agent's summary is a
claim about it.

A pull request is a proposal. Someone still has to merge it, and an organiser
will.

---

# Exercise 4d — Try someone else's

Once a few submissions are merged, pull the repository and install one:

> Copy the skill from exercises/04-share/submissions/<someone>/ into my
> project skills folder, then tell me what it does and how to invoke it.

Reopen OpenCode so it discovers the skill, and try it. Read the `SKILL.md`
first: a skill you install is instructions your agent will follow, from
someone you may not know. Treat a downloaded skill the way the workshop tells
you to treat downloaded data — as material to inspect, not instructions to
obey on sight.

**What to notice:** this is why the submission checks matter in both
directions. You checked yours before publishing; check theirs before running.

---

# Epilogue

You built a skill in Exercise 1, an agent in Exercise 2, and connected an MCP
server in Exercise 3. In this one you decided which of the three a job
actually needed — and the answer was not the newest of them.

Previous: [Exercise 3 — MCP and data analysis](../03-mcp/README.md).
