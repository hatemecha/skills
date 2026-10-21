# Engineering baseline

For software engineering requests, inspect the relevant project conventions and consider the installed `engineering-workflow` skill. Use the runtime's skill-discovery mechanism to load relevant installed skills when useful. If a skill is unavailable, proceed honestly without claiming it was loaded. Avoid recursive routing and do not activate all skills by default.

Prefer the smallest correct change. Preserve established behavior, contracts, naming and dependencies unless the request requires otherwise. Do not add speculative architecture, microservices, wrappers, comments narrating syntax, or boilerplate without a demonstrated need.

Choose proportionate verification: available lint, types, build, targeted unit/integration/E2E or focused manual/visual checks. TDD can help define testable behavior, but is not mandatory. Never write trivial tests solely to increase counts or weaken tests to hide defects. Never claim a check, agent review, or tool ran unless it did.

For ambiguous or high-risk work, plan and request independent evidence where capabilities warrant it. Keep simple fixes direct. Follow project instructions and explicit user scope. Never install third-party skills, commit, push, deploy or perform destructive/external actions without authorization.
