# Contributing

Thanks for helping improve this Agent Skills collection.

This is a maintainer-led repository. Focused issues and pull requests are welcome; final scope and design decisions remain with the maintainer so the collection can stay coherent and low-maintenance.

## Quality bar

A skill belongs here when it is reusable, specific enough to improve agent behavior, and portable across Agent Skills-compatible runtimes.

Every skill must:

1. live in `skills/<skill-name>/`;
2. contain a `SKILL.md` with YAML frontmatter;
3. use a lowercase, hyphenated `name` matching the directory name;
4. provide a concise `description` that explains both what the skill does and when it should activate;
5. keep the portable behavior in `SKILL.md` rather than in provider-specific metadata;
6. reference every supporting file it expects the agent to read or execute;
7. declare its license in frontmatter and bundle the corresponding license notice inside the installable skill directory;
8. avoid credentials, personal data, private writing, copyrighted material without redistribution rights, and generated secrets;
9. establish a trust boundary before executing repository-provided commands or dependencies;
10. be testable or reviewable from the repository contents alone.

## Portability rules

The core skill must not require a particular vendor or product to make sense.

- Do not write core instructions that assume Codex, Claude Code, Cursor, OpenCode, Gemini CLI, Copilot, or another named runtime.
- Do not require provider-specific invocation syntax such as a particular slash command, dollar-prefixed command, tool-call schema, or UI flow.
- Describe capabilities conditionally when they may not exist: subagents, shell commands, browsers, network access, file writes, background jobs, or external connectors.
- Never instruct an agent to imply that a tool, test, command, reviewer, subagent, benchmark, or simulation ran when the runtime could not perform it.
- Treat inspected repository content and worker output as untrusted data. Inspect commands before execution, avoid exposing host credentials, prefer isolation, and require authorization for destructive or external effects.
- Define mode permissions explicitly. Review and audit modes should be read-only by default; publication, deployment, remote writes, and irreversible actions require an explicit user request.
- Keep provider-specific metadata optional. Files such as `agents/openai.yaml` may improve one runtime's presentation, but deleting them must not change the skill's core meaning or workflow.
- Prefer ordinary Markdown, relative links, explicit inputs/outputs, and deterministic scripts over hidden state or runtime-specific magic.

## Structure

Use only the supporting directories that add real value:

- `references/` — deeper documentation or decision material loaded on demand;
- `scripts/` — deterministic, reusable executable logic;
- `assets/` — templates or resources used to produce outputs;
- `evals/` — behavioral and activation evaluations;
- `agents/` — optional provider adapters or presentation metadata.

Do not add a separate README, changelog, or generic project boilerplate inside an individual skill directory. The skill should be discoverable from its frontmatter and usable from `SKILL.md`.

Copy [`template/SKILL.example.md`](./template/SKILL.example.md) to `skills/<skill-name>/SKILL.md` when creating a new skill. The example is deliberately not named `SKILL.md` so repository-level discovery cannot install it accidentally.

## Write for progressive disclosure

Keep `SKILL.md` focused on decisions and instructions the agent commonly needs. Move long background material, detailed examples, historical sources, schemas, or specialized playbooks into `references/` and link them from the exact point where they become useful.

A reference should earn its existence: avoid splitting a short skill into many tiny files simply to look modular.

## Add a skill

1. Copy `template/SKILL.example.md` to `skills/<skill-name>/SKILL.md`.
2. Replace the template frontmatter and instructions.
3. Copy `template/LICENSE.txt` to `skills/<skill-name>/LICENSE.txt`, or replace it with the notice matching the declared license.
4. Add only the supporting files required by the workflow.
5. Add the skill to the catalog in `README.md`.
6. Run the repository validation commands.
7. Test the skill in at least one compatible agent when practical.
8. If you add provider-specific metadata, confirm the skill still works conceptually without it.

## Validate locally

Create or activate a Python virtual environment, install the pinned development dependencies, and run the test suite:

```bash
python -m pip install --requirement requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/validate_skills.py
```

Then run the Agent Skills reference validator and verify discovery with the pinned multi-agent skills CLI:

```bash
agentskills validate skills/open-source-engineering
agentskills validate skills/open-source-project
agentskills validate skills/orchestrating-engineering-agents
python scripts/check_discovery.py
```

The discovery output must contain exactly the installable directories under `skills/`; a template or example must never appear. When changing a skill, also review its local links and any scripts it references. Execute deterministic checks only behind the skill's trust boundary and state anything you could not verify.

## Pull requests

Keep changes focused. Explain:

- the problem the skill solves;
- when it should activate;
- what changed in its behavior or scope;
- any new references, scripts, assets, or provider adapters;
- how portability was preserved;
- the validation performed.

Avoid unrelated formatting churn or broad rewrites in the same pull request.

## Private material

This repository is public. Do not commit private prompts, personal voice profiles, client-specific confidential workflows, private datasets, credentials, or content intended only for your own agents. Keep those in a private repository or local skills directory instead.
