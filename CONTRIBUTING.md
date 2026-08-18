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
7. avoid credentials, personal data, private writing, copyrighted material without redistribution rights, and generated secrets;
8. be testable or reviewable from the repository contents alone.

## Portability rules

The core skill must not require a particular vendor or product to make sense.

- Do not write core instructions that assume Codex, Claude Code, Cursor, OpenCode, Gemini CLI, Copilot, or another named runtime.
- Do not require provider-specific invocation syntax such as a particular slash command, dollar-prefixed command, tool-call schema, or UI flow.
- Describe capabilities conditionally when they may not exist: subagents, shell commands, browsers, network access, file writes, background jobs, or external connectors.
- Never instruct an agent to imply that a tool, test, command, reviewer, subagent, benchmark, or simulation ran when the runtime could not perform it.
- Keep provider-specific metadata optional. Files such as `agents/openai.yaml` may improve one runtime's presentation, but deleting them must not change the skill's core meaning or workflow.
- Prefer ordinary Markdown, relative links, explicit inputs/outputs, and deterministic scripts over hidden state or runtime-specific magic.

## Structure

Use only the supporting directories that add real value:

- `references/` — deeper documentation or decision material loaded on demand;
- `scripts/` — deterministic, reusable executable logic;
- `assets/` — templates or resources used to produce outputs;
- `agents/` — optional provider adapters or presentation metadata.

Do not add a separate README, changelog, or generic project boilerplate inside an individual skill directory. The skill should be discoverable from its frontmatter and usable from `SKILL.md`.

Start from [`template/SKILL.md`](./template/SKILL.md) when creating a new skill.

## Write for progressive disclosure

Keep `SKILL.md` focused on decisions and instructions the agent commonly needs. Move long background material, detailed examples, historical sources, schemas, or specialized playbooks into `references/` and link them from the exact point where they become useful.

A reference should earn its existence: avoid splitting a short skill into many tiny files simply to look modular.

## Add a skill

1. Copy `template/SKILL.md` to `skills/<skill-name>/SKILL.md`.
2. Replace the template frontmatter and instructions.
3. Add only the supporting files required by the workflow.
4. Add the skill to the catalog in `README.md`.
5. Run the repository validation commands.
6. Test the skill in at least one compatible agent when practical.
7. If you add provider-specific metadata, confirm the skill still works conceptually without it.

## Validate locally

Run the repository validator:

```bash
python scripts/validate_skills.py
```

Then verify discovery with the open multi-agent skills CLI:

```bash
npx skills add . --list
```

When changing a skill, also review its local links and any scripts it references. Execute deterministic checks when the environment permits and state anything you could not verify.

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
