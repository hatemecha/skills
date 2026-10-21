# Skills

Personal, portable [Agent Skills](https://agentskills.io/specification) for software engineering with Codex, Cursor, OpenCode, and other compatible agents. The aim is **less unnecessary code and more verified behavior**, not more process. This is a personal toolkit, not a polished community framework.

## Quick start

Install the whole catalog globally (Node.js and `npx` required):

```bash
npx skills add hatemecha/skills --list
npx skills add hatemecha/skills -g --skill '*' -a codex -a cursor -a opencode
```

For proactive usage across projects, also install the short global rules. They are **separate** from the skill installation and are not applied by `npx skills add`:

```bash
git clone https://github.com/hatemecha/skills.git
cd skills
python scripts/install_agent_rules.py          # preview only
python scripts/install_agent_rules.py --apply  # Codex + OpenCode
```

Cursor User Rules must be pasted manually: run `python scripts/install_agent_rules.py --print-cursor` and paste the output into **Cursor Settings → Rules → User Rules**. Do not paste it into a project-specific rule unless that scope is intended.

**Full instructions, Windows/PowerShell, remote agents, reinstall/update, safety:** [Installation guide](docs/installation.md).

## How proactive routing works

- The global rules tell the agent to **consider** `engineering-workflow` on coding work.
- `engineering-workflow` classifies intent and risk, then loads relevant skills through each runtime's documented mechanism when possible.
- Simple changes stay simple. Debugging, design, test strategy, independent review and handoff are conditional.
- Skill selection is model-dependent; global rules and metadata improve activation, **not guarantee it**. See [routing evaluations](docs/evaluation.md).

## Catalog

| Skill | When it helps |
| --- | --- |
| [engineering-workflow](skills/engineering-workflow) | Entry point: select a proportionate workflow and relevant skills |
| [open-source-engineering](skills/open-source-engineering) | Scoped implementation, refactoring, design and code review |
| [systematic-debugging](skills/systematic-debugging) | Root cause, regressions and failing behavior |
| [test-strategy](skills/test-strategy) | Unit/integration/E2E/static verification and conditional TDD |
| [engineering-brainstorming](skills/engineering-brainstorming) | Ambiguous features, game mechanics, significant design |
| [orchestrating-engineering-agents](skills/orchestrating-engineering-agents) | Evidence-gated parallel/independent work when warranted |
| [context-handoff](skills/context-handoff) | Transfer real project state between agents or sessions |
| [open-source-project](skills/open-source-project) | Licensing, public repository readiness, releases and governance |

You can still invoke one directly, e.g. “Use systematic-debugging to investigate this regression.”

## Principles

- Inspect the relevant code first. Preserve established contracts.
- Favor straightforward designs over speculative layers or fashionable architecture.
- Treat TDD, game design documents, multi-agent workflows, and E2E as **tools**, not universal rituals.
- Run relevant checks; never claim simulated tests or reviews.
- Only use verified installed skills. Do not automatically install third-party skills.
- Keep project-specific instructions in that project's own `AGENTS.md` rather than copying every workflow there.

See [CONTRIBUTING.md](CONTRIBUTING.md) for validation, packaging, trust boundaries and development standards.

## License

[MIT](LICENSE).
