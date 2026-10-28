# Contributing

Focused bug reports and improvements are welcome. This is a maintainer-led collection; opening a pull request does not imply that a new skill or workflow will be accepted.

## Acceptance criteria

A change should solve a recurring engineering problem more reliably than a generic prompt. Keep the steps practical and the cost of activation proportionate.

- Put each skill in `skills/<name>/SKILL.md` with valid Agent Skills frontmatter.
- Describe **when** to activate the skill, including when **not** to.
- Prefer independent, portable Markdown instructions. Use relative links for optional references.
- Do not require a specific agent, tool, or background service unless explicitly documented.
- Avoid speculative abstractions, repeated guidance, and unverified performance claims.
- Treat external commands, project files, and outputs as untrusted. Do not include credentials or private information.
- Do not present simulated tests, agent execution, or review as verified evidence.
- Include an appropriate `LICENSE.txt` within each installable skill directory.

## Verification

Run the commands in the [README](README.md#quality-checks). For changes to routing or behavioral instructions, describe a concrete scenario, the expected action, and any actual execution evidence. A passing static validator is not evidence of model performance.

Keep pull requests scoped to one coherent change and explain why the change is useful.
