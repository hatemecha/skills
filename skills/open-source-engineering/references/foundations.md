# Foundations and source map

This reference explains where the skill's principles come from and, just as importantly, what the skill is **not** claiming.

The traditions below overlap historically and technically, but they are not one doctrine. Unix engineering, SICP, pragmatic programming, Agile, Linux kernel maintainability, free software, and later open-source practice have different origins and goals. The skill synthesizes compatible engineering habits without pretending that their authors agreed on a single methodology.

## 1. Free software: users should be able to understand and change their computing

### Primary source

- GNU Project / Free Software Foundation, **The Free Software Definition**: https://www.gnu.org/philosophy/free-sw.en.html

GNU defines free software around the user's freedom to run, study, modify, redistribute, and share modified versions of a program. Access to source code is a prerequisite for studying and modifying it.

### Engineering interpretation used by this skill

The legal and ethical freedoms do not prescribe a coding style, but they create a useful engineering consequence: software intended to be meaningfully modifiable should not be unnecessarily opaque.

That supports preferences for:

- understandable source;
- inspectable behavior;
- documented interfaces and formats;
- replaceable components;
- reproducible or at least understandable build steps;
- useful diagnostics;
- avoiding artificial technical lock-in.

Do not reverse this implication. Readable or modular code is not automatically free/open-source software. Licensing and distribution conditions still matter; use `$open-source-project` for that assessment.

## 2. Unix: small tools, composition, early trial, and leverage

### Primary/archival source

- Nokia Bell Labs, **Creating a programming philosophy from pipes and a tool box**: https://www.nokia.com/bell-labs/unix-history/philosophy.html

The Bell Labs archive describes the Unix tool approach associated with Doug McIlroy, including programs that do one thing well, work together, and communicate through useful interfaces. Contemporary Unix guidance also emphasized trying software early and using tools to reduce repeated labor.

### Engineering interpretation used by this skill

The transferable principles are:

- cohesive responsibilities;
- composition over monolithic accumulation;
- simple interfaces that enable unforeseen combinations;
- useful intermediate representations;
- building and testing real slices early;
- tool leverage instead of repetitive manual work.

### What not to cargo-cult

"Do one thing well" does **not** mean every class must contain one method, every module must become a process, or every system should become microservices.

The useful unit is a **coherent responsibility with a clear interface**. A well-designed monolith can follow Unix-like modular principles internally; a fleet of tiny services can violate them through coupling and operational complexity.

Plain text is powerful when human inspectability, pipelines, diffs, and interoperability benefit from it. It is not mandatory when a database, binary format, strongly typed protocol, or domain-specific representation is more appropriate.

## 3. SICP: abstraction, modularity, and programs as expressions of knowledge

### Primary source

- MIT Press, **Structure and Interpretation of Computer Programs, 2nd ed.**: https://mitpress.mit.edu/9780262510875/structure-and-interpretation-of-computer-programs/
- MIT CSAIL, **SICP video lectures**: https://groups.csail.mit.edu/mac/classes/6.001/abelson-sussman-lectures/

MIT describes SICP as emphasizing fundamental models of computation, abstraction, modularity, and programming languages as vehicles for expressing knowledge.

### Engineering interpretation used by this skill

A useful abstraction should make an idea easier to state and reason about. It should compress **conceptual knowledge**, not merely move syntax elsewhere.

This leads to:

- names that expose the domain idea;
- procedural/data abstraction when it reduces what callers must know;
- modular boundaries that localize change;
- explicit computational models for stateful or complex behavior;
- evaluating abstractions by how much reasoning they remove.

An abstraction that introduces more concepts than it hides is usually premature.

## 4. The Pragmatic Programmer: DRY, orthogonality, reversibility, tools, and testing

### Primary publisher sources

- Pragmatic Bookshelf, **Pragmatic Programmer Tips**: https://pragprog.com/tips/
- Pragmatic Bookshelf, **The Pragmatic Programmer, 20th Anniversary Edition**: https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/

The publisher's official tips define DRY in terms of a single authoritative representation of **knowledge**, not a ban on repeated text. The book also develops orthogonality, reversibility, plain-text/tool leverage, debugging, contracts, and strong testing practices.

### Engineering interpretation used by this skill

#### DRY

Ask whether two places encode the same rule or fact. If a requirement changes, should both places change for the same reason?

- If yes, centralization may remove duplicated knowledge.
- If no, merging them can create a false abstraction and unwanted coupling.

Duplicated syntax is sometimes cheaper than shared machinery with the wrong semantics.

#### Orthogonality

Prefer parts that can change independently. A feature edit should not require unrelated configuration, database, UI, and infrastructure changes unless the domain genuinely connects them.

#### Reversibility

Avoid architecture that makes ordinary decisions unnecessarily irreversible. Use boundaries around volatile external services and make large changes in reviewable steps.

#### Tools

Automate mechanical repetition when the automation itself is simpler and more reliable than recurring manual work.

## 5. Agile: working software, technical excellence, adaptation, and work not done

### Primary source

- **Principles behind the Agile Manifesto**: https://agilemanifesto.org/principles

Relevant principles include working software as the primary measure of progress, continuous attention to technical excellence and good design, adaptation to change, sustainable development, and simplicity as maximizing unnecessary work avoided.

### Engineering interpretation used by this skill

- prefer a working vertical slice over speculative infrastructure;
- design enough for the current constraints while keeping the code easy to change;
- keep feedback loops short;
- do not count scaffolding, diagrams, abstractions, or generated code as progress if the required behavior still does not work;
- remove unnecessary planned work rather than merely implementing it faster.

"Respond to change" does not justify architecture with extension points for every imaginable future. Change-friendly software usually comes from clear boundaries and low coupling, not maximal configurability.

## 6. Linux kernel maintainability: shallow reasoning and straightforward code

### Primary source

- Linux kernel documentation, **Linux kernel coding style**: https://docs.kernel.org/process/coding-style.html

The kernel coding-style document explicitly treats deep indentation as a warning, encourages short functions that do one thing well, and discourages tricky expressions. Its motivation is maintainability and readability under demanding conditions.

### Engineering interpretation used by this skill

Use these as diagnostic signals:

- deep nesting can mean too many decisions are active simultaneously;
- many local variables can signal excess responsibility;
- long complex functions can be hard to hold in working memory;
- clever expressions can hide state transitions and error cases;
- descriptive helpers can reduce cognitive load.

### What not to cargo-cult

Kernel-specific formatting exists for the kernel's language, tooling, history, and review culture. Do not impose its tabs, braces, or exact line-width preferences on Rust, Python, JavaScript, PHP, Kotlin, or another project's established formatter.

The transferable lesson is **reduce cognitive complexity**, not "make all repositories look like kernel C."

## 7. KISS as a synthesis heuristic

This skill uses **KISS** as shorthand for a broad recurring engineering preference: do not introduce more mechanism than the real problem requires.

It intentionally does not depend on a disputed origin story or a rigid historical attribution.

Operationally, KISS means:

- choose direct language features before frameworks when both solve the problem safely;
- avoid speculative generality;
- minimize the number of concepts needed to explain the solution;
- avoid unnecessary runtime states and transitions;
- keep exceptional paths explicit;
- prefer boring, familiar technology when novelty provides no concrete advantage.

KISS does not mean "write the fewest lines". A few extra explicit lines can be much simpler than a compressed generic abstraction.

## 8. The combined engineering model

The skill synthesizes the traditions into six questions:

1. **Can a human understand the code?** — SICP, kernel maintainability.
2. **Is each piece responsible for coherent knowledge?** — Unix, DRY, orthogonality.
3. **Can pieces be combined and replaced through clear boundaries?** — Unix, pragmatic reversibility, open engineering.
4. **Did we avoid work and machinery that the current problem does not require?** — Agile simplicity, KISS.
5. **Does the software actually work, and can we prove the relevant behavior?** — Agile working software, pragmatic testing.
6. **Can users and future maintainers inspect, diagnose, modify, and migrate the system without unnecessary dependence?** — free-software/open-source tradition.

When these principles conflict, preserve correctness first, then choose the design that minimizes total cognitive and operational complexity for the actual system.

## 9. Conflict-resolution examples

### DRY vs simplicity

Three similar blocks may be easier to understand than a generic abstraction with callbacks, flags, and type parameters. Do not centralize until the shared knowledge is clear.

### Small functions vs locality

Extracting every five lines into helpers can make reading harder by forcing constant navigation. Keep code together when the steps form one simple narrative and no reusable concept is exposed.

### Composition vs performance

A clean pipeline may allocate or copy too much in a measured hot path. Optimize the bottleneck while preserving the clearest boundary possible, and document the reason for the exception.

### User control vs product constraints

A hosted collaborative product may genuinely require network services. Open engineering means minimizing unnecessary captivity and documenting/exporting user data where possible, not pretending every application can be offline-first.

### Stable architecture vs change

Do not rebuild the architecture for every feature. Do not freeze a boundary that repeatedly causes cross-cutting edits either. Let repeated evidence reveal where the real seam belongs.

## 10. Historical precision

When explaining the philosophy to users:

- distinguish **free software** as a freedom-centered movement from **open source** as a later term and movement with overlapping software practices;
- do not attribute all Unix practice to one person;
- do not present KISS, DRY, Agile, SICP, and kernel style as one historical lineage;
- say that this skill is a modern synthesis of compatible engineering lessons.

The synthesis is deliberate; the history should remain accurate.