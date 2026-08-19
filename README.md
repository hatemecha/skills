# Skills

Portable Agent Skills for software engineering and open-source project work.

This repository follows the [Agent Skills specification](https://agentskills.io/specification): each skill is self-contained, uses a standard `SKILL.md`, and keeps provider-specific integrations optional.

## Install

```bash
npx skills add hatemecha/skills --list
npx skills add hatemecha/skills
npx skills add hatemecha/skills --skill open-source-engineering
```

Use `-g` for a global installation. See the [`skills` CLI](https://github.com/vercel-labs/skills) for agent targeting and `--all` behavior.

You can also copy a skill directory into the skills path used by any Agent Skills-compatible runtime.

## Catalog

| Skill | Purpose |
| --- | --- |
| [`open-source-engineering`](./skills/open-source-engineering) | Design, implement, refactor, and review software with a bias toward simplicity, readability, and low technical debt. |
| [`open-source-project`](./skills/open-source-project) | Create, convert, audit, and prepare genuinely open-source projects. |
| [`orchestrating-engineering-agents`](./skills/orchestrating-engineering-agents) | Run multi-agent engineering work with bounded roles and evidence gates. |

## Usage

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

- `SKILL.md` is the portable source of truth.
- Core instructions do not assume a specific agent runtime.
- Provider-specific metadata belongs in optional adapter files such as `agents/openai.yaml`.
- Supporting files live in `references/`, `scripts/`, `assets/`, or `evals/` only when they materially improve the skill.
- Every installable skill carries its own license notice.
- Skills that may execute repository-provided commands establish a trust boundary first.
- A skill must not claim that a command, test, review, or tool ran when the runtime cannot execute it.

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full quality bar.

## Creating a skill

Copy [`template/SKILL.example.md`](./template/SKILL.example.md) to `skills/<skill-name>/SKILL.md` and copy `template/LICENSE.txt` beside it. Keep the main file focused on instructions the agent needs for the task. Put background in `references/` only when a specific mode needs it.

Before submitting changes:

```bash
python -m pip install --requirement requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_skills.py
agentskills validate skills/open-source-engineering
agentskills validate skills/open-source-project
agentskills validate skills/orchestrating-engineering-agents
python scripts/check_discovery.py
```

## Contributing

Focused issues and pull requests are welcome. This is a maintainer-led collection. Read [CONTRIBUTING.md](./CONTRIBUTING.md) before adding or changing a skill.

## License

Available under the [MIT License](./LICENSE).
