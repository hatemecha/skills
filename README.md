# Skills

Reusable [Agent Skills](https://agentskills.io/specification) for software engineering. Designed to work with compatible coding agents, with no runtime service or proprietary dependency.

The collection favors small changes, explicit constraints, and verification proportional to risk. Each skill can be used independently; `engineering-workflow` helps select the others when needed.

## Install

Inspect the available skills before installing:

```sh
npx skills add hatemecha/skills --list
npx skills add hatemecha/skills -g -a codex -a cursor -a opencode
```

Requires Node.js and a compatible version of the [skills CLI](https://github.com/vercel-labs/skills). Review any prompts before replacing existing skills. Verify local installation using `npx skills list -g`.

## Skills

| Skill | Purpose |
| --- | --- |
| [engineering-workflow](skills/engineering-workflow/SKILL.md) | Select a proportionate workflow and relevant installed skills |
| [open-source-engineering](skills/open-source-engineering/SKILL.md) | Implement, refactor, simplify, and review maintainable software |
| [systematic-debugging](skills/systematic-debugging/SKILL.md) | Diagnose regressions and unexpected behavior using evidence |
| [test-strategy](skills/test-strategy/SKILL.md) | Choose useful unit, integration, E2E, or manual checks |
| [engineering-brainstorming](skills/engineering-brainstorming/SKILL.md) | Resolve important design uncertainty before implementation |
| [orchestrating-engineering-agents](skills/orchestrating-engineering-agents/SKILL.md) | Coordinate independent work and evidence-based reviews |
| [context-handoff](skills/context-handoff/SKILL.md) | Transfer verified state between agents and sessions |
| [open-source-project](skills/open-source-project/SKILL.md) | Assess licensing, publication readiness, and project health |

### Optional automatic routing

Some agents do not automatically select a skill for every appropriate task. A compact global policy is available at [config/global-engineering-rules.md](config/global-engineering-rules.md). Installing the skills **does not** install this policy.

For Codex and OpenCode, preview the proposed edits before applying them:

```sh
python scripts/install_agent_rules.py
python scripts/install_agent_rules.py --apply
```

The script preserves unrelated instructions in the target files. For Cursor, run `python scripts/install_agent_rules.py --print-cursor` and paste the text into **Settings → Rules → User Rules**. Check existing rules for contradictions first.

Routing remains model- and runtime-dependent. A skill cannot guarantee another skill loads, invoke an unavailable subagent, or reduce context usage by itself.

## Quality checks

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_skills.py
for skill in skills/*; do agentskills validate "$skill"; done
```

CI checks metadata, packaging, links, local installer behavior, and the Agent Skills format. These checks **do not** establish that a model always selects the correct skill or that the pack improves coding results. Such claims require controlled agent runs with trace and outcome evidence.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the scope and review criteria.

## License

[MIT](LICENSE). Each installable skill includes its own license notice.
