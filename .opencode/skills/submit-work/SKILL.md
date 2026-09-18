---
name: submit-work
description: Share a skill, agent or MCP configuration to the workshop repository as a pull request. Use when the user wants to submit, publish or push their own work to the shared workshop repo, not for general git work in an unrelated project.
---

# Submit work to the workshop repository

Publish the user's own skill, agent or MCP configuration into
`exercises/04-share/submissions/<name>/` in the workshop repository, as a
pull request from their fork.

Publishing is public and hard to take back. A deleted commit stays in the
fork's history and in anyone's clone. Check before pushing, not after.

## Establish what is being shared

Identify the files the user actually wants to share, and where they are. A
skill is a folder with `SKILL.md`; an agent is one Markdown file; an MCP
contribution is the server block from `opencode.json` plus notes. Copy them
into `exercises/04-share/submissions/<name>/` — do not move them, so the
user's working setup keeps running.

Choose `<name>` with the user. Use their name or GitHub handle, lowercase
with hyphens. Never write into another person's submission folder, and never
modify files elsewhere in the repository.

## Check before publishing, and show the user

Run these and report the results before committing anything:

1. **What would be committed.** `git status --short` and `git diff --cached`.
   Read the actual file list. Do not rely on your own expectation of it.

2. **Nothing is silently ignored.** The repository's `.gitignore` excludes
   common folder names, so a submission in a folder called `build`, `dist`,
   `lib`, `var`, `target`, `venv`, `env`, `downloads`, `sdist`, `wheels` or
   `eggs` disappears without any error. Verify every intended file:

   ```bash
   git check-ignore -v exercises/04-share/submissions/<name>/*
   ```

   No output means nothing is ignored. Any output names a file that will not
   ship. Rename the folder rather than editing the shared `.gitignore`.

3. **No credentials.** Search the staged files for API keys, tokens,
   passwords and personal paths. The workshop keeps keys out of the
   repository. If anything looks like a secret, stop and tell the user.

4. **No large or generated files.** Databases, caches, `node_modules`,
   downloaded datasets and build products do not belong in a submission.
   State the total size. Anything over a few hundred KB needs a reason.

5. **It is self-contained.** A skill folder needs its `SKILL.md` and any
   file it references. Copying `SKILL.md` alone leaves a skill incomplete.

Report what each check found. Distinguish checks that passed, that failed,
and that you could not run.

## Publish

Students do not have write access to the workshop repository, so the work
goes through a fork:

```bash
gh repo fork <workshop-repo> --clone --remote      # once
git checkout -b submit-<name>
git add exercises/04-share/submissions/<name>
git commit -m "Add <name> submission: <what it is>"
git push -u origin submit-<name>
gh pr create --title "..." --body "..."
```

Ask before the push and before creating the pull request: those two steps are
the ones that publish. If `gh` is missing or not authenticated, say so and
stop rather than inventing another route.

Commit only the submission folder. Never use `git push --force`,
`git reset --hard`, or any command that rewrites shared history. If the push
is rejected, report the error and let the user decide.

## Hand over

Give the user the pull request URL, list what was included, and state
anything you did not check. Do not claim the submission was accepted — it has
been proposed, and someone still has to merge it.
