# Additional resources

Further reading and projects to explore after the workshop. These are resources to inspect, not endorsements or automatic installation instructions.

## Where to go after today

| Project | What to explore |
|---|---|
| [OpenCode](https://opencode.ai/) | The workshop harness: [v2 documentation](https://opencode.ai/v2/docs/) and [source code](https://github.com/anomalyco/opencode) |
| [awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) | A map of plugins, themes, agents and projects |
| [oh-my-pi](https://github.com/can1357/oh-my-pi) | An alternative harness with integrated development tools |
| [OpenAgentsControl](https://github.com/darrenhinde/OpenAgentsControl) | Planning and approval-based agent coordination |
| [python-expert-agent](https://github.com/amrahman90/python-expert-agent) | A compact, domain-specific agent package to inspect |

Read installation scripts and check compatibility before running them.
Popularity is not a security review.

## Paper2Agent: papers as usable tools

Paper2Agent turns a paper and its associated code into an **MCP server**,
with tools an agent can use to run the paper's methods.

Its workflow executes and tests code rather than relying on a summary of
the manuscript alone. The paper includes collaborating agents that
prioritise a candidate causal gene for psoriasis.

**Why it matters:** a research contribution can become something others
interrogate and reuse. Computational prioritisation still needs biological validation.

[Miao et al., Nature, 16 September 2026](https://www.nature.com/articles/s41586-026-11044-y)

Thank you, Chiao-Yu, for pointing us to this! A preprint appeared in 2025.

## Multimodal agents: beyond text and tables

**Multimodal** means working across data types.
**Multi-agent** means dividing work across agents. A system can do both.

An illustrative research workflow:

1. Inspect microscopy images with an image-capable model or analysis tool.
2. Calculate measurements and relate them to sample metadata.
3. Produce a report that links each conclusion to its evidence.

Generating a plot does not mean the agent has visually inspected it.
Check which data types its model and tools actually support.

## Biomedical agents and their evaluation

**[Biomni](https://biomni.stanford.edu/)** brings biomedical tools and databases
into an agent environment for research tasks across biological domains.

**[BixBench](https://arxiv.org/abs/2503.00096)** evaluates agents on practical
biological analyses requiring multiple steps and interpretation.

Together, they suggest two research questions: what can we connect, and
how do we establish that the resulting system works?

**What evidence would convince you to use an agent's result in your research?**

## Three things to take away

1. **Separate instructions, execution and permissions.** Know what each
   component contributes and what it can access.

2. **Expose the tools the task needs.** Descriptions and results can consume
   context. The overhead depends on the harness and configuration.

3. **Validate the scientific result.** Successful execution does not establish
   correct methods, interpretation or reproducibility.

[github.com/peterwadsackett/AgenticWorkshop](https://github.com/peterwadsackett/AgenticWorkshop)

## References: research and further reading

- **Paper2Agent.** Miao et al. (2026). *Reimagining research papers as interactive and reliable AI agents.* Nature. [doi:10.1038/s41586-026-11044-y](https://doi.org/10.1038/s41586-026-11044-y). [Earlier preprint](https://arxiv.org/abs/2509.06917).
- **Biomni.** *A General-Purpose Biomedical AI Agent.* [Research paper](https://doi.org/10.1101/2025.05.30.656746), [project and current publication links](https://biomni.stanford.edu/).
- **BixBench.** Mitchener et al. (2025). *A Comprehensive Benchmark for LLM-based Agents in Computational Biology.* [arXiv:2503.00096](https://arxiv.org/abs/2503.00096).
- **Protein Data Bank.** Berman et al. (2000). Nucleic Acids Research 28:235–242. [doi:10.1093/nar/28.1.235](https://doi.org/10.1093/nar/28.1.235).
- **The resolution revolution.** Kühlbrandt (2014). Science 343:1443–1444. Background for the cryo-EM discussion. [doi:10.1126/science.1251652](https://doi.org/10.1126/science.1251652).

## References: tools and security

- **OpenCode v2:** [overview](https://opencode.ai/v2/docs/) · [skills](https://opencode.ai/v2/docs/skills/) · [agents](https://opencode.ai/v2/docs/agents/) · [permissions](https://opencode.ai/v2/docs/permissions/).
- **OpenCode extensions:** [MCP servers](https://opencode.ai/v2/docs/mcp-servers/) · [plugins](https://opencode.ai/v2/docs/plugins/).
- **Model Context Protocol:** [documentation](https://modelcontextprotocol.io/docs/getting-started/intro).
- **OWASP:** [MCP Tool Poisoning](https://owasp.org/www-community/attacks/MCP_Tool_Poisoning). Further reading on malicious instructions embedded in tool descriptions or responses.

Project links are on “Where to go after today”. Check current documentation,
installation scripts and data-handling terms before trying them.
