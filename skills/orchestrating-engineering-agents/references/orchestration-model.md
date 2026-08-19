# Orchestration model

Use this when choosing roles, risk routes, state transitions, or parallel execution. A role exists only when separating that responsibility increases independence, focus, or evidence quality.

## Role pool

| Role | Activate when | Must not own alone |
| --- | --- | --- |
| Orchestrator | Multi-step or multi-agent work | Final technical truth without evidence |
| Planner | Multiple dependencies or uncertainty | Sole implementation approval |
| Architect | Cross-cutting or structurally significant change | Final acceptance after authoring the design and implementation |
| Builder | Code or configuration must change | Sole review of its own change |
| Verifier | Any material implementation | Rewriting criteria merely to obtain green results |
| Adversarial Reviewer | Security, permissions, untrusted input, data integrity, concurrency, high risk | Product-policy decisions for the user |
| Quality Reviewer | Medium+ change or significant refactor | Replacing executable correctness checks |

One worker may hold compatible roles when risk is low. Separate author and final approver.

## Risk routing

Assess security, data loss, compatibility, concurrency, architecture, deployment, and requirement uncertainty.

- **Low:** local, reversible, narrow, well-tested. Builder -> deterministic verification.
- **Medium:** multiple files, behavior change, user-visible workflow. Planner if needed -> Builder -> independent Verifier/Reviewer.
- **High:** auth, secrets, migrations, public APIs, concurrency, production impact. Architect -> Builder -> Verifier -> Adversarial Reviewer.
- **Critical:** severe or irreversible impact. High-risk topology plus a human gate before the irreversible action.

## Control plane

```text
PROPOSED -> TRIAGED -> PLANNED -> READY -> IMPLEMENTING -> VERIFYING -> REVIEWING -> ACCEPTED
```

Any active state may become `BLOCKED`, `NEEDS_HUMAN`, or `REJECTED`. Recovery: `VERIFYING`/`REVIEWING` back to `IMPLEMENTING` or `PLANNED`. A worker cannot advance global state by returning a success message.

## Parallelism and retries

Parallelize independent analysis, test design, threat analysis, or isolated implementation slices. Serialize edits to the same file, schema-plus-consumers, shared fixtures, and lockfile upgrades.

Independent reviewers should receive the requirements and the artifact, not the implementer's conclusion. Shared model, prompt, and context count as correlated evidence.

Classify a failure before retrying: implementation, plan, requirement, test, or environment. Default to two repair cycles for the same root cause.
