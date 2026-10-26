---
name: context-handoff
description: Transfer an active software task between Codex, Cursor, OpenCode, agents, computers, or sessions without losing decisions and real verification state. Use when explicitly handing off or resuming work, not after every trivial change.
license: MIT
---

# Context Handoff

Summarize verified state without substituting the handoff for the repository.

## When to use a checkpoint

Use one for an explicit handoff or resumption, impending context limits, or a meaningful boundary in long-running work. Do not create recurring notes after every command or for straightforward fixes. A checkpoint is a compact current-state snapshot, not a transcript or a replacement for Git.

## Procedure

1. Inspect the current tree/diff, relevant instructions, decisions, and any observed test results. If git or execution is unavailable, say so.
2. Produce a compact, current-state handoff with: goal and acceptance criteria; repo/ref and working-tree status; changes made and affected files; immutable constraints; decisions and reasons; commands actually run with outcomes and evidence paths; unverified risks; exact next action. Prefer pointers to code and evidence over pasted file bodies or huge logs.
3. Distinguish **done**, **in progress**, **blocked**, and **planned**. Mark unknowns and facts needing revalidation. Never turn a proposal or worker claim into completed work.
4. Keep secrets, tokens, personal data and logs containing them out of the handoff.
5. Refresh an existing checkpoint by replacing stale claims instead of appending repeated historical summaries. Preserve unresolved requirements, failure evidence, and compatibility constraints.
6. Prefer a response or ephemeral artifact. Write persistent notes only if asked or if the existing project workflow already uses them. Do not duplicate AGENTS.md, README or plans unnecessarily.

## Cross-runtime

Use portable Markdown and file paths. Do not assume a particular agent has access to another agent's memory, terminal state, private skills, or uncommitted files. Specify precisely what the receiving agent must inspect. On resumption, verify the live branch/diff and evidence before continuing; the handoff may be stale. Use native context compaction only when the runtime supports it. This skill cannot itself erase earlier conversation turns.

## Permissions

Read-only by default; never commit, push, upload or modify project files solely to create a handoff without authorization.

## Template

- Goal and acceptance criteria
- Repository/ref/dirty files (or unknown)
- Completed changes with evidence locations
- Decisions and relevant constraints
- Checks actually executed; checks skipped
- Open issues / risks
- Next action
