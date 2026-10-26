# Install and update

Requirements: modern Node.js with `npx`, Python 3.10+, and local access to Codex, Cursor or OpenCode. No installation command here touches production projects automatically.

## 1. Install or update skills

```bash
npx skills add hatemecha/skills --list
npx skills add hatemecha/skills -g --skill '*' -a codex -a cursor -a opencode
```

Inspect prompts before accepting replacement of an already installed skill. Verify discovery with `npx skills list -g` and `npx skills check`. On subsequent updates, use `npx skills update -g`; if the old installation lacks new catalog entries, rerun the `skills add` command. The three runtimes discover the same local `~/.agents/skills/` path in their documented configurations.

Don't run `npx skills add ... --copy` from a directory that is also the destination `.agents/skills`. Prefer the remote source as shown above. Run `npx skills --help` if your CLI's flags have changed.

## 2. Install minimal proactive rules

Skill metadata alone cannot force a model to call the entry-point skill. Add a short global policy as a separate step:

```bash
git clone https://github.com/hatemecha/skills.git
cd skills
python scripts/install_agent_rules.py
python scripts/install_agent_rules.py --apply
```

PowerShell on Windows (if `python` is not on PATH, try `py`):

```powershell
git clone https://github.com/hatemecha/skills.git
Set-Location skills
py scripts/install_agent_rules.py
py scripts/install_agent_rules.py --apply
```

The installer only targets `~/.codex/AGENTS.md` and `~/.config/opencode/AGENTS.md`, on the **current machine and user account**. Preview is the default; `--apply` appends or updates only a marked section, keeping unrelated content intact. It refuses malformed markers and symlinks. Check the diff before applying if you customized either file.

**Cursor:** open Settings → Rules → User Rules and paste the exact text from:

```bash
python scripts/install_agent_rules.py --print-cursor
```

Cursor User Rules are not a portable file; the script deliberately does not automate settings changes. If you already have global rules, merge thoughtfully rather than pasting contradictory duplicates.

Restart or open a new agent session so it can discover the updated files.

### Refresh an existing setup

In a previously cloned `skills` directory, run `git pull --ff-only` and then `python scripts/install_agent_rules.py --apply` (use `py` on Windows if necessary). Re-run `npx skills update -g` to refresh installed skills; use the `npx skills add hatemecha/skills -g --skill '*' -a codex -a cursor -a opencode` command if new entries are missing. Reprint and replace the managed text in Cursor User Rules with `python scripts/install_agent_rules.py --print-cursor`, avoiding duplicates.

No separate package or runtime is required for the new context-efficiency guidance. Native context compaction, when available, is a separate runtime capability; these instructions alone cannot shorten existing chat history or guarantee token savings.

## 3. Check that routing works

Try: “Fix this small bug in the smallest scope and use the relevant installed engineering skills; report checks actually run.” Then ask: “Which installed skills did you load, and why?” No claim of activation is proof without observing the runtime's skill call or tool trace. Follow [evaluation guide](evaluation.md) for repeatable scenarios.

## Project and remote agents

The global policy is intentionally small. Maintain project-specific build commands, architecture and constraints in each project's `AGENTS.md` when appropriate. Avoid copying every installed skill into that file.

Global skills and rules are local to each machine/user. For remote SSH, container, CI or cloud agents, install in that runtime or provide project-local `.agents/skills/` and `AGENTS.md` as needed. Cursor Cloud Agents do **not** automatically receive `~/.agents/skills/`; see Cursor's **Sync Skills for Cloud Agents** feature for skills kept under `~/.cursor/skills/`.

## Security and limitations

- Do not run untrusted third-party skills or scripts without inspection.
- Global policy increases the likelihood of routing, not deterministic skill invocation.
- A skill cannot itself guarantee that another skill loads or that a fresh independent reviewer exists.
- The installer does not install skills, replace global Cursor preferences, change project files, push code, or set up a background agent.
- The repository's CI checks package validity and routing *fixtures*, not model adherence.

References: [Agent Skills](https://agentskills.io/specification), [OpenCode skills](https://opencode.ai/docs/skills), [OpenCode rules](https://opencode.ai/docs/rules), [Cursor skills](https://cursor.com/help/customization/skills), [Cursor rules](https://cursor.com/docs/rules), [skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md).
