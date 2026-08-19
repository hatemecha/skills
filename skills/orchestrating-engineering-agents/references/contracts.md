# Contracts and evidence ledger

Workers should exchange artifacts and evidence, not conversational summaries. Use YAML, JSON, or an in-memory structure. Do not create repository files solely to satisfy this reference.

Keep acceptance criteria observable. Avoid criteria such as "clean" or "secure" unless they are decomposed into verifiable properties.

## Task contract

```yaml
task:
  id: AUTH-014
  objective: Allow users to reset a forgotten password safely.
  non_goals:
    - Redesign account settings.
  acceptance_criteria:
    - Reset tokens expire after 30 minutes.
    - Reset tokens can be used only once.
    - The response does not reveal whether an email is registered.
  affected_surfaces: [authentication, email, database]
  invariants:
    - Existing sessions remain valid unless product policy says otherwise.
  risk: high
  required_evidence: [unit tests, integration tests, security review]
```

## Work packet

```yaml
work_packet:
  id: AUTH-014-impl
  role: builder
  objective: Implement single-use password reset tokens.
  write_scope: [src/auth/, tests/auth/]
  required_checks: [targeted tests, type-check]
  stop_conditions:
    - Token reuse is rejected.
    - Existing login tests still pass.
```

## Worker result

Report the artifact produced, commands actually run, evidence, unresolved findings, and whether the packet is complete, blocked, or needs a human. Do not claim a check ran if it did not.

## Ledger

Append decisions, state transitions, evidence, and residual risk. The ledger is the source of truth for why the task advanced.
