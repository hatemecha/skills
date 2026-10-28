# Engineering Skills

[English](README.md) · [Español](README.es.md)

A focused collection of reusable [Agent Skills](https://agentskills.io/specification) for software development. Each skill provides practical guidance for a specific kind of work, from designing a feature to debugging and reviewing code.

Designed for compatible coding agents, including Codex, Cursor, and OpenCode.

## Installation

```bash
npx skills add hatemecha/skills
```

To make the skills available across projects, use `-g`:

```bash
npx skills add hatemecha/skills -g
```

You can also [browse the collection on skills.sh](https://skills.sh/hatemecha/skills).

## Skills

### Engineering

| Skill | What it does |
| --- | --- |
| [Engineering Workflow](skills/engineering-workflow/SKILL.md) | Selects the right approach and relevant skills for a coding task without adding unnecessary process. |
| [Open Source Engineering](skills/open-source-engineering/SKILL.md) | Guides implementation, refactoring, and code review toward clear, maintainable solutions. |
| [Systematic Debugging](skills/systematic-debugging/SKILL.md) | Investigates failures through reproduction, evidence, and root-cause analysis. |
| [Test Strategy](skills/test-strategy/SKILL.md) | Chooses meaningful tests and verification methods based on the changes and risks. |

### Design & coordination

| Skill | What it does |
| --- | --- |
| [Engineering Brainstorming](skills/engineering-brainstorming/SKILL.md) | Turns unclear requirements into a small, implementable design. |
| [Orchestrating Engineering Agents](skills/orchestrating-engineering-agents/SKILL.md) | Coordinates independent agents and evidence-based reviews when the task warrants them. |
| [Context Handoff](skills/context-handoff/SKILL.md) | Carries decisions, progress, and verified results between agents or sessions. |

### Open source

| Skill | What it does |
| --- | --- |
| [Open Source Project](skills/open-source-project/SKILL.md) | Reviews licensing, documentation, and readiness for public release. |

## Usage

Ask your agent to use a skill by name, for example:

> Use `systematic-debugging` to investigate this regression.

For broader tasks, start with `engineering-workflow` to identify which skills are useful. Skill discovery and automatic activation depend on your agent.

## Contributing

Focused improvements and bug reports are welcome. See [Contributing](CONTRIBUTING.md).

## License

[MIT](LICENSE).
