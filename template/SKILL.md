---
name: example-skill
description: Describe what this skill does and the situations in which an agent should use it. Keep activation guidance concrete and vendor-neutral.
---

# Example Skill

State the outcome this skill helps the agent produce and the principles that should guide the work.

## Core rules

1. Put the highest-value behavioral rules here.
2. Keep instructions independent of any specific agent or model vendor.
3. Treat optional capabilities conditionally when they may not exist.
4. Require evidence before claiming that work was executed or verified.
5. Keep the workflow proportionate to the task.

## Workflow

### 1. Inspect the task

Identify the objective, constraints, relevant inputs, existing instructions, and evidence required for completion.

### 2. Choose the smallest useful approach

Prefer a direct workflow. Add references, scripts, tools, or additional agents only when they materially improve the result.

### 3. Execute

Perform the requested work while preserving user scope and repository or project conventions.

### 4. Verify

Use the strongest relevant checks available in the current runtime. If a capability is unavailable, state the limitation instead of fabricating execution.

## Supporting resources

Use these directories only when needed:

- `references/` for detailed material loaded on demand;
- `scripts/` for deterministic reusable logic;
- `assets/` for templates or output resources;
- `agents/` for optional provider-specific metadata that is not required by the core skill.

Link every required supporting file from `SKILL.md` at the point where the agent should use it.

## Completion

Describe the expected result, evidence, remaining uncertainty, and any material next steps.
