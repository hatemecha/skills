# Evaluate skill selection (not just YAML)

The repository's validators check installability and route-fixture consistency. They **do not run coding models** or demonstrate reliable automatic activation.

Use [routing-cases.json](../evals/routing-cases.json) as a manually executable evaluation set.

## Protocol

1. Run each prompt in a disposable example repository with an appropriate fixture. Note model, runtime, installed skill versions, settings, and baseline behavior.
2. Compare **without** the global rules and **with** the global rules, keeping all other conditions as similar as possible.
3. Inspect actual runtime traces for skill loads; an agent's claim that it used a skill is not sufficient.
4. Mark required, optional, and excluded skill selections. Explicit noncoding cases should not invoke engineering skills.
5. Score outcome correctness, unrelated file churn, meaningful verification, tokens/time if available, and user interventions. The same run may satisfy skills selection but still fail on code quality.
6. Repeat across Codex, Cursor and OpenCode. Don't merge apparent improvements from different models as if they were controlled measurements.

Record concrete results and failures manually. Never generate synthetic "passes" for model behavior; adjust routing descriptions only after observing repeated failure patterns.

## Context-efficiency trials

Run at least one short, clear change and one long, multi-step task in the same disposable repository. Compare existing and revised instructions with the same model, task fixture, and available tools. Record whether native compaction, caching, or fresh-context features were active; they can change costs independently of these skills.

Capture runtime-reported input/output tokens and wall time **only when available**, plus number of tool calls, repeated reads, relevant failures preserved, task correctness, and required user interventions. If actual usage is unavailable, mark it unknown rather than estimating a percentage. Inspect execution traces to check whether checkpoints were created only when justified, resumed state was verified, and source evidence survived context reduction.

The paper [SKILL.state](https://arxiv.org/html/2608.26263v2) evaluates a *runtime* that replaces historical transcripts with validated structured state. These Markdown instructions do not reproduce that runtime, and its reported savings are not predictions for Codex, Cursor, or OpenCode.

## What each fixture means

- `must_use`: skills expected for the test's scenario, if actually installed and discoverable.
- `may_use`: defensible but not mandatory choices.
- `must_not_use`: evidence of unnecessary activation if loaded.
- `success`: human-observable outcome, not an automated assertion about model quality.

CI validates only the fixture schema, uniqueness and consistency. It does not infer tool calls from prose.
