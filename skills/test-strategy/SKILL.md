---
name: test-strategy
description: Choose and implement proportionate verification for changed software behavior: unit, integration, end-to-end, contract, static checks, or focused manual testing. Use when a feature or bug fix needs evidence; decide whether TDD is useful instead of mandating tests for every detail.
license: MIT
---

# Test Strategy

Tests protect behaviors and risks, not line counts. Prefer the lowest-cost reliable evidence for the change.

## Select evidence by risk

- **Pure business logic, calculations, parsing, algorithms:** focused unit/property tests, ideally with a clear failing example first when it reduces ambiguity.
- **Module contracts, persistence, authorization, APIs:** integration/contract tests at the real boundary; mock only dependencies beyond that boundary.
- **Critical user journeys:** targeted E2E covering outcomes visible to users, not every variation of static UI text.
- **Visual tweaks:** inspect actual UI or screenshots when possible; type/lint/build and a targeted visual check may be more informative than a new unit test.
- **Small structural refactor:** existing behavioral tests and static checks may be enough if they cover the invariant.
- **No viable harness:** do not create a major framework solely for a trivial change. Document manual checks and the evidence gap.

## TDD decision

Use red-green-refactor when a stable observable contract exists, a failing test can be written cheaply, and it helps specify the behavior. Do not force TDD for exploratory spikes, artwork, CSS placement, or undefined requirements. Never modify tests merely to make an incorrect implementation pass.

## Verification sequence

1. Identify the behavior and realistic failure modes.
2. Choose the smallest checks that exercise them. Reuse project tools before adding dependencies.
3. Make changes; include a focused regression test for a reproduced bug when practical.
4. Run actual lint/type/build/test/E2E commands appropriate to the changed surface. Check skipped or quarantined tests.
5. Separate verified facts from assertions and residual risks.

Treat tests, scripts, package hooks, network calls and fixtures as untrusted until inspected. Do not run destructive suites or production writes without permission. This skill does not authorize commits, pushes or deployment.

## Output

State what was tested, with which commands or steps, and why the chosen scope is sufficient; identify what was not executed.
