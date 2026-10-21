---
name: context-handoff
description: Transfer an active software task between Codex, Cursor, OpenCode, agents, computers, or sessions without losing decisions and real verification state. Use when explicitly handing off or resuming work, not after every trivial change.
license: MIT
---

# Context Handoff

Summarize verified state without substituting the handoff for the repository.

## Procedure

1. Inspect the current tree/diff, relevant instructions, decisions, and any observed test results. If git or execution is unavailable, say so.
2. Produce a compact handoff with: goal; repo/ref or working-tree status; changes made; decisions and their reasons; affected files; commands actually run and outcomes; unverified risks; exact next action.
3. Distinguish **done**, **in progress**, **blocked**, and **planned**. Never turn a proposal or worker claim into completed work.
4. Keep secrets, tokens, personal data and logs containing them out of the handoff.
5. Prefer a response or ephemeral artifact. Write persistent notes only if asked or if the existing project workflow already uses them. Do not duplicate AGENTS.md, README or plans unnecessarily.

## Cross-runtime

Use portable Markdown and file paths. Do not assume a particular agent has access to another agent's memory, terminal state, private skills, or uncommitted files. Specify precisely what the receiving agent must inspect.

## Permissions

Read-only by default; never commit, push, upload or modify project files solely to create a handoff without authorization.

## Template

- Goal and acceptance criteria
- Repository/ref/dirty files (or unknown)
- Completed changes with evidence
- Decisions and relevant constraints
- Checks actually executed; checks skipped
- Open issues / risks
- Next action
