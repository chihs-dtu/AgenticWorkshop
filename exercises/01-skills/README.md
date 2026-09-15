# Exercise 1 — Building and improving skills

## 1a — Peter's skill examples

Follow Peter's [existing skill exercises](../../workflow.md). They cover
PDB downloads, downloading an existing rendered structure image, and moving
skills between projects. His instructions remain in that document.

## 1b — A skill that helps make skills

Inspect [skill-builder](../../.opencode/skills/skill-builder/SKILL.md).
It helps an agent clarify a skill's purpose, write useful instructions,
choose supporting files, and check the result. It is itself a skill, not
a separate agent or a newly trained model.

Example request in OpenCode Plan mode:

> Use skill-builder to review the skill I just created. Explain which
> instructions are useful, what is missing, and how we could test it.
> Propose changes before implementing them.

## 1c — Make and test your own skill

Choose a small task you want to repeat. Use skill-builder to define its
inputs, outputs, and checks. Review the proposal before switching to Build
mode and authorizing implementation.

The skill belongs in `.opencode/skills/<skill-name>/SKILL.md`. Give each skill
its own subfolder. Add scripts, references, or assets only when they help.

Test one successful request, one invalid or incomplete input, and a different
valid input. Inspect the outputs yourself. Record what passed and what you
have not tested, then revise the skill in response to actual failures.

Next: [Exercise 2a and 2b — agents](../02-agents/README.md).
