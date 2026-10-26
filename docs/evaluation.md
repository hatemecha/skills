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

## Reproducible trials in disposable repositories

Three small, intentionally limited Python fixtures live in [benchmark-cases.json](../evals/benchmark-cases.json). They exercise a minimal edit, a persistence regression and a new capacity feature. Their baseline tests are checked in CI: the tiny edit is already green, while the two behavioral tasks deliberately start failing. These **do not** prove agent performance.

Create separate workspaces without overwriting previous trials:

```bash
python scripts/prepare_eval_case.py regression baseline
python scripts/prepare_eval_case.py regression skills
```

Open each workspace in a supported agent with the exact prompt from the manifest, a new session, equivalent permissions, model and environment. Run the same tests after agent work: `python -m unittest discover -s . -p "test_*.py"`. Inspect the final diff and actual test output yourself. Use a separate agent profile with no global skills/rules for baseline; verify the effective loaded instructions and avoid editing your real home configuration as a benchmark shortcut.

Capture raw traces when possible: `codex exec --json`, `opencode run --format json`, or `agent -p --output-format stream-json` (check the installed CLI's help). Save them outside Git, redact credentials, private data and sensitive prompts, and independently inspect actual skill-load events. An agent stating that it used a skill is not trace evidence. These commands can write files and run commands; use only disposable repositories and restricted permissions.

### Recording runs

Create `evals/results/runs.jsonl` (ignored by Git). Store **one JSON object per completed run**; `baseline` and `skills` must have identical `case_id`, `runtime`, `model`, `environment` and `trial`. Example schema (illustrative only; not an executed result):

```json
{"case_id":"regression","runtime":"codex","model":"model-id","environment":"linux-test","trial":1,"variant":"skills","outcome":"unknown","evidence":"","trace_checked":false,"loaded_skills":[],"input_tokens":null,"output_tokens":null,"elapsed_seconds":null,"unrelated_changes":null}
```

- `outcome`: `pass`, `fail` or `unknown`. A claimed `pass` must include a concrete `evidence` reference to test output or a reviewed artifact. The tool **does not check that reference itself**.
- `trace_checked`: set true only after examining the runtime trace for actual skill invocations. Fill `loaded_skills` from observed events, not the assistant's prose. A baseline that loads pack skills is contaminated.
- `input_tokens`/`output_tokens`: only populate from runtime-reported usage. Missing numbers remain null. Cursor may not report comparable token totals.
- `trial`: use paired repetition indices (0, 1, 2...) to compare the same task independently. Preserve all failures and skipped checks.

After recording both variants:

```bash
python scripts/evaluate_agent_runs.py evals/results/runs.jsonl
python scripts/evaluate_agent_runs.py evals/results/runs.jsonl --json
```

The evaluator pairs runs by task, runtime, model, environment and trial; reports routing only with inspected traces; and reports token deltas only when both variants contain complete usage. It **does not call models, validate test claims, inspect raw traces or infer token savings**. Compare results within the same model/runtime; do not pool them indiscriminately. For long handoffs, security work and visual tasks, the original routing cases remain manual until suitable fixtures exist.
