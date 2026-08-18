# Skills

Portable, reusable Agent Skills for software engineering and repository work.

This repository follows the open [Agent Skills specification](https://agentskills.io/specification): each skill is self-contained, uses a standard `SKILL.md`, and keeps provider-specific integrations optional. The core instructions are designed to work with any agent that can consume Agent Skills rather than depending on a single model, vendor, or CLI.

## Install

List the available skills:

```bash
npx skills add hatemecha/skills --list
```

Install interactively for the agents detected on your machine:

```bash
npx skills add hatemecha/skills
```

Install one skill:

```bash
npx skills add hatemecha/skills --skill open-source-engineering
```

Target one or more supported agents when you want explicit placement:

```bash
npx skills add hatemecha/skills --skill open-source-engineering -a cursor -a claude-code
```

Use `-g` for a global installation or `--all` to install all skills for all detected agents. See the [`skills` CLI](https://github.com/vercel-labs/skills) for the current agent list and install options.

You can also copy a skill directory manually into the skills directory used by an Agent Skills-compatible runtime.

## Catalog

| Skill | Purpose |
| --- | --- |
| [`open-source-engineering`](./skills/open-source-engineering) | Design, implement, refactor, and review software with a strong bias toward simplicity, readability, composability, evidence, and low technical debt. |
| [`open-source-project`](./skills/open-source-project) | Create, convert, audit, and prepare genuinely open-source projects, including licensing, documentation, governance, portability, privacy, and release readiness. |
| [`orchestrating-engineering-agents`](./skills/orchestrating-engineering-agents) | Design or execute adaptive multi-agent engineering workflows with bounded roles, evidence gates, independent review, and evaluation. |

## Usage

Agents that support automatic skill discovery can activate a skill from its frontmatter description. You can also request it by name without relying on provider-specific invocation syntax.

```text
Use the open-source-engineering skill to review this module, preserve behavior, remove unnecessary complexity, and verify the refactor.
```

```text
Use the open-source-project skill to prepare this repository for a public open-source release and report any blockers.
```

```text
Use the orchestrating-engineering-agents skill to implement this feature with the smallest useful multi-agent topology and independent verification.
```

## Portability contract

Every skill in this repository should satisfy these rules:

- `SKILL.md` is the portable source of truth.
- Required frontmatter is limited to standard Agent Skills fields unless a field is demonstrably portable.
- Core instructions do not assume Codex, Claude Code, Cursor, OpenCode, Gemini CLI, Copilot, or any other specific runtime.
- Capabilities such as subagents, shell access, browsers, network access, or file writes are treated conditionally when they may not exist.
- Provider-specific metadata belongs in optional adapter files such as `agents/openai.yaml`; removing those adapters must not break the skill itself.
- Supporting content uses relative links and lives in `references/`, `scripts/`, or `assets/` only when it materially improves the skill.
- A skill must not claim that a command, test, review, subagent, or tool ran when the current runtime cannot actually execute it.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full quality bar.

## Repository structure

```text
skills/
├── skills/
│   ├── open-source-engineering/
│   │   ├── agents/          # optional provider adapters
│   │   ├── references/
│   │   └── SKILL.md
│   ├── open-source-project/
│   │   ├── agents/
│   │   ├── references/
│   │   └── SKILL.md
│   └── orchestrating-engineering-agents/
│       ├── agents/
│       ├── references/
│       └── SKILL.md
├── template/
│   └── SKILL.md
├── scripts/
│   └── validate_skills.py
├── .github/
│   └── workflows/
│       └── validate-skills.yml
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Creating a skill

Start from [`template/SKILL.md`](./template/SKILL.md), then keep the main file focused on the instructions that should be loaded for the task. Put detailed background material in `references/`, deterministic reusable logic in `scripts/`, and output resources in `assets/`.

Before submitting changes, run:

```bash
python scripts/validate_skills.py
npx skills add . --list
```

## Design principles

This collection favors skills that are:

- **portable** — useful across agents and runtimes;
- **self-contained** — understandable without hidden prompts or private infrastructure;
- **progressively disclosed** — concise core instructions with deeper references loaded only when useful;
- **evidence-driven** — explicit about what was inspected, executed, verified, or left uncertain;
- **maintainable** — clear scope, minimal duplication, and no speculative complexity;
- **honest about capabilities** — graceful degradation instead of fabricated execution.

## Contributing

Focused issues and pull requests are welcome. This is a maintainer-led collection; inclusion is based on usefulness, portability, clarity, and maintenance cost. Read [CONTRIBUTING.md](./CONTRIBUTING.md) before adding or changing a skill.

## License

Available under the [MIT License](./LICENSE).
