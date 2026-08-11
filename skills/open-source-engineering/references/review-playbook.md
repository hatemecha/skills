# Review and refactoring playbook

Use this reference when auditing an existing codebase, reviewing a change, or simplifying code that has accumulated technical debt.

The purpose is not to maximize the number of findings. The purpose is to identify the **smallest set of structural changes that materially reduces the cost and risk of future change**.

## 1. Start with behavior, not aesthetics

Before calling code "bad", determine:

- what behavior it implements;
- who depends on that behavior;
- which inputs and edge cases matter;
- whether tests capture the intended behavior;
- whether the code sits on a public API, persisted schema, protocol, migration, or compatibility boundary;
- whether a strange implementation exists for a documented performance or platform reason.

Do not refactor around an unverified assumption.

## 2. Review order

Review in this order so superficial cleanup does not hide deeper problems.

### A. Correctness and invariants

Look for:

- contradictory conditions;
- invalid states that can be constructed;
- unchecked error paths;
- partial updates;
- stale caches or derived state;
- race-prone state changes;
- missing transaction boundaries;
- inconsistent validation;
- silent fallback behavior;
- data-loss paths;
- error handling that converts failure into apparent success.

Fix correctness before style.

### B. Knowledge duplication

Search for the same rule represented in multiple places:

- validation limits;
- status/state definitions;
- permission logic;
- price/tax/discount calculations;
- path construction;
- feature flags;
- retry policies;
- protocol constants;
- schema field meaning;
- transformation rules;
- configuration defaults.

Ask: **If this requirement changes, which locations must change for the same reason?**

If several locations must move together, centralize the knowledge at the most natural owner.

Do not centralize code merely because it has the same shape.

### C. Responsibility and cohesion

For each function/module/class/component, ask:

- Can its responsibility be described precisely in one sentence?
- Does it mix domain decisions with transport, persistence, rendering, or logging?
- Does it change for several unrelated reasons?
- Does it expose internals because callers need to coordinate its steps manually?
- Does it contain branches for concepts that belong to separate workflows?

Split when there are distinct reasons to change. Keep together when steps form one cohesive operation.

### D. Coupling and dependency direction

Look for:

- domain logic importing UI/framework details;
- persistence models leaking through every layer;
- components reaching into each other's internals;
- shared mutable global state;
- service locators or registries used as hidden dependencies;
- circular dependencies;
- configuration read directly from arbitrary business logic;
- one feature requiring edits in many unrelated modules.

Prefer dependencies that point toward stable domain concepts. Put volatile infrastructure behind narrow boundaries where that actually reduces coupling.

### E. Control-flow complexity

Warnings include:

- deep nesting;
- long chains of `else if`/`elif` with mixed responsibilities;
- boolean parameters changing major behavior;
- many flags that create combinatorial states;
- repeated early/late cleanup paths;
- exception-driven ordinary control flow;
- state encoded by combinations of nullable fields;
- loops that mutate many external variables.

Possible simplifications:

- guard clauses;
- named predicates;
- explicit state objects/enums;
- table-driven mappings;
- separating calculation from effects;
- extracting a real sub-operation;
- reducing the number of legal states.

Do not replace a simple conditional with polymorphism merely to remove an `if`.

### F. Data flow

Trace important values from input to output.

Ask:

- Where is the value created?
- Where is it normalized or validated?
- Who owns mutation?
- Is the same value transformed repeatedly?
- Does a caller need hidden knowledge about sequencing?
- Are there multiple representations with unclear authority?
- Can state be immutable for longer?

Prefer one authoritative representation at each stage and explicit transitions between representations.

### G. Abstraction quality

Smells:

- interface with one implementation and no boundary reason;
- base class with one subclass;
- factory that only invokes one constructor;
- generic wrapper whose callers still need implementation details;
- configuration-driven behavior with only one real configuration;
- callbacks/generics that make two simple cases harder to read;
- utilities containing unrelated helpers;
- abstractions named `Manager`, `Service`, `Processor`, `Handler`, `Common`, or `Utils` without a precise responsibility.

Do not delete these automatically. Identify whether they protect a real boundary, external dependency, ownership rule, test seam, or known variation.

A good abstraction should remove knowledge from its callers.

### H. Dependencies

For each notable dependency, especially new ones, ask:

- What real problem does it solve?
- Could the existing stack solve it with less total complexity?
- Is this security- or standards-sensitive work where mature reuse is safer?
- Does it add runtime, build, supply-chain, binary-size, or platform costs?
- Is it widely used throughout the codebase or imported for one trivial helper?
- Can it be upgraded or replaced without rewriting the domain?

Removing dependencies is not automatically virtuous. Reimplementing cryptography, authentication protocols, parsers, database engines, image codecs, or other difficult standards can dramatically increase risk.

### I. Error handling and observability

Look for:

- swallowed errors;
- catch-all exceptions;
- duplicate logging at every layer;
- errors without operation/context;
- logs that expose secrets;
- retries with no limit or backoff rationale;
- `null`, empty string, zero, or `false` used as ambiguous failure values;
- background jobs that can fail invisibly;
- generic "something went wrong" diagnostics where actionable context is available.

A failure path should be understandable from logs/errors without reconstructing the whole call stack manually.

### J. Tests

Look for both missing tests and misleading tests.

Warnings:

- tests assert implementation details rather than behavior;
- every collaborator is mocked;
- snapshots cover logic that deserves explicit assertions;
- unit tests pass while integration boundaries are untested;
- a bug fix has no regression test despite being reproducible;
- tests duplicate production algorithms;
- flaky timing or real-network tests hide nondeterminism;
- fixtures are so large that test intent is invisible.

Prefer tests that make the contract obvious and fail for one meaningful reason.

### K. Performance

Do not infer performance from code aesthetics.

Require evidence for claims such as:

- "this allocation is expensive";
- "this cache is necessary";
- "async is faster";
- "parallelism will help";
- "this query is too slow";
- "we need a lower-level language here".

Check realistic input sizes, complexity, I/O behavior, profiler data, query plans, memory use, or benchmarks as appropriate.

If no measurement exists and users are not experiencing a performance constraint, prefer the clearer design.

### L. Open engineering and user control

When relevant to the product, inspect:

- undocumented proprietary formats;
- user data with no export path;
- hard-coded SaaS providers;
- unnecessary mandatory network calls;
- configuration that cannot be reproduced outside one control plane;
- hidden generated artifacts required to build;
- telemetry without clear disclosure;
- replaceable components coupled directly throughout the domain.

Do not demand local-first or plain text for products whose core requirements genuinely need other designs. Identify unnecessary lock-in, not unavoidable infrastructure.

## 3. Heuristics that trigger investigation

These are prompts for review, not pass/fail metrics.

| Signal | Question to ask |
| --- | --- |
| More than ~3 meaningful nesting levels | Are too many decisions active in one scope? |
| Function no longer fits comfortably in one mental view | Does it contain multiple responsibilities or phases? |
| Many local variables | Is the function managing too much state? |
| Boolean parameter changes major behavior | Are there really two operations hidden in one API? |
| Many optional/null fields | Is state being modeled implicitly? |
| Same condition repeated across modules | Is a domain rule duplicated? |
| Small change touches many layers | Is knowledge leaking across boundaries? |
| Single change requires synchronized edits in several places | Is there more than one authority for the same fact? |
| Generic abstraction has one real user | Was generality introduced before evidence? |
| Helper reduces line count but hides intent | Is indirection costing more than it saves? |
| New dependency for a tiny operation | Is the maintenance cost justified? |
| Mock-heavy tests | Are boundaries artificial or dependencies hidden? |
| Comment explains each line | Could naming/control flow make the code self-explanatory? |
| Cache/queue/async added without measurements | Is complexity solving a demonstrated constraint? |

The Linux kernel's well-known warnings about deep nesting, long complex functions, and many locals are useful because they correlate with cognitive load, not because the exact numbers transfer to every language.

## 4. Common AI-generated smells

Agents often generate structure by analogy to familiar enterprise patterns. Review especially for:

### Layer multiplication

Example shape:

```text
Controller
  -> Service
    -> Manager
      -> Repository
        -> Adapter
          -> Client
```

This can be valid in a complex system, but every layer must own a distinct concern. If several layers simply rename and forward arguments, collapse them.

### Premature genericity

Warning signs:

- generic type parameters with one concrete use;
- strategy registries containing one strategy;
- pluggable backends with no requested second backend;
- configuration toggles for hypothetical modes;
- abstract base classes created at the same time as their only subclass.

Prefer concrete code until a real variation point is visible.

### Helper fragmentation

A file can become harder to read after being "cleaned" into dozens of tiny private helpers. Extract when the helper names a real concept, removes repeated reasoning, or isolates a boundary—not merely because the original function became long.

### Pattern worship

Patterns are vocabulary for recurring design problems, not objectives. Do not add factories, builders, visitors, mediators, observers, CQRS, event buses, hexagonal layers, or domain events unless the problem actually benefits from them.

### Defensive noise

Agents may add redundant checks everywhere because they cannot prove invariants. Instead:

1. determine where the invariant should be established;
2. validate it there;
3. make downstream code rely on the established contract when safe in the language/runtime.

Repeated defensive checks can obscure which states are truly legal.

### Comment inflation

Remove comments that paraphrase syntax. Keep comments that explain:

- why an unusual choice exists;
- external constraints;
- non-obvious invariants;
- compatibility hacks;
- performance evidence;
- security assumptions;
- consequences that are not visible from the code.

## 5. Refactoring patterns that usually pay off

Use only when evidence supports them.

### Replace nesting with explicit exits

Good when invalid/precondition/terminal cases can be handled first and the main path becomes linear.

Avoid when many early returns make resource lifetime or state mutation harder to follow.

### Extract a named decision

Good when a complex predicate encodes domain knowledge.

Bad when `isValid()` merely hides several unrelated checks callers need to understand differently.

### Move knowledge to its owner

Good when several callers duplicate the same invariant or calculation.

Choose the owner based on the domain concept, not whichever file is easiest to edit.

### Replace flag combinations with explicit state

Good when multiple booleans or nullable fields create invalid combinations.

Use an enum/state type/state machine only if there is a genuine state model. Do not create machinery for a simple two-branch condition.

### Separate pure decision from effect

Good when I/O obscures business logic or makes behavior hard to test.

Example conceptual split:

```text
parse/validate -> decide -> persist/send/render
```

Do not force functional purity across an entire codebase when the language/framework makes a straightforward imperative flow clearer.

### Collapse pass-through layers

Good when a layer owns no policy, transformation, lifecycle, boundary, or observability responsibility.

Keep it when it intentionally shields the domain from a volatile external system or provides a stable contract.

### Introduce a boundary around volatility

Good for third-party APIs, operating-system integration, clocks, randomness, payment providers, storage engines, or external transports when the rest of the application should not know their details.

Avoid creating adapters for stable local code solely to satisfy a diagram.

## 6. Prioritizing findings

Score mentally across four dimensions:

- **Impact:** correctness, security, operability, or maintenance cost;
- **Frequency:** how often the affected area changes or runs;
- **Spread:** how much of the system the problem touches;
- **Fix risk:** how dangerous or expensive the correction is.

Prefer findings with high impact/frequency/spread and a tractable fix.

A small naming issue in a core invariant can be more important than a 500-line file that rarely changes and is easy to understand.

## 7. Refactoring stop conditions

Stop when:

- the requested behavior is clear and verified;
- the relevant knowledge has an obvious owner;
- the main path is straightforward to follow;
- remaining duplication represents different concepts or is cheaper than abstraction;
- further splitting would mostly increase navigation;
- further generalization only anticipates hypothetical requirements;
- performance is adequate for measured workloads;
- remaining debt is outside the task's change boundary.

A refactor is successful when the next likely change requires less reasoning and fewer coordinated edits—not when the code reaches a theoretical purity score.

## 8. Suggested review report

Use a compact report like:

```text
Summary
- Main structural risk: ...
- Strongest simplification opportunity: ...
- Verification available: ...

Critical
1. [location] Problem -> evidence -> smallest safe fix -> risk

Structural
1. ...

Simplification
1. ...

Polish
1. ...

Recommended order
1. Protect behavior with ...
2. Fix ...
3. Simplify ...
4. Re-run ...
```

Omit empty sections. Keep evidence close to each finding. Prefer five strong findings over twenty speculative ones.