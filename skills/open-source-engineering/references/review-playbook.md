# Review and refactoring playbook

Use this when auditing an existing codebase or simplifying accumulated debt. Identify the smallest structural changes that reduce the cost and risk of future change.

## Review order

1. **Behavior first.** Establish what the code does, who depends on it, which tests capture intent, and whether a strange implementation exists for a documented performance or platform reason.
2. **Correctness.** Contradictory conditions, constructible invalid states, swallowed errors, partial updates, race-prone mutations, data-loss paths, and handlers that convert failure into apparent success.
3. **Knowledge duplication.** If a requirement changes, which locations must change for the same reason? Centralize that knowledge. Do not merge code that only looks similar.
4. **Cohesion and coupling.** Split mixed reasons to change. Keep a single operation together. Prefer dependencies that point toward stable domain concepts.
5. **Control flow and data flow.** Treat deep nesting, flag explosion, and hidden mutation as warnings. Trace important values from input to output and keep one authoritative representation at each stage.
6. **Abstractions and dependencies.** Keep an abstraction only if it owns a named piece of knowledge and makes callers simpler. Add a dependency only when it removes more risk than it introduces.
7. **Tests.** Protect decisions and behavior, not incidental structure. Excess mocking often means the boundary is fake.

Fix correctness before style. Do not start with a cosmetic rewrite.

## Safe refactor order

1. Strengthen behavioral coverage for the affected path.
2. Remove proven-dead code.
3. Improve names and make invariants visible.
4. Simplify control flow.
5. Separate mixed responsibilities.
6. Centralize duplicated knowledge.
7. Remove abstractions or dependencies that no longer pay for themselves.
8. Optimize only measured bottlenecks.
9. Rerun verification after meaningful steps.

## What to report

Prefer a short set of structural findings over a long list of nits. For each finding: location, problem, consequence, evidence, smallest improvement, and breakage risk.
