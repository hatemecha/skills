# Proportional standard for open-source repositories

## Contents

1. Level 0: not publishable
2. Level 1: valid open foundation
3. Level 2: healthy open project
4. Level 3: well-governed project
5. Project-specific needs
6. Review rubric
7. Primary references

## 1. Level 0: not publishable

Resolve any of these blockers before presenting a project as open source:

- no open-source license;
- insufficient rights to publish;
- missing essential source;
- secrets or personal data;
- use restrictions incompatible with open source;
- undeclared mandatory private infrastructure;
- malicious or deceptive behavior;
- third-party artifacts that cannot legally be redistributed.

## 2. Level 1: valid open foundation

Minimum requirements:

- a clear, compatible license;
- preferred source form;
- README with purpose, status, and basic instructions;
- reproducible installation or execution;
- declared dependencies;
- no known secrets;
- preserved attribution;
- disclosed limitations and closed components;
- public issue-reporting channel;
- reasonable version history.

This level supports publication but does not imply that contribution or maintenance is easy.

## 3. Level 2: healthy open project

Add what fits the project:

- concise contribution, conduct, security, and support policies;
- automated tests and CI;
- formatter, lint, and lockfiles;
- issue and pull request templates;
- architecture documentation;
- examples and test data;
- release notes or changelog;
- versioning and compatibility policy;
- dependency updates and reproducible releases;
- data export and migration;
- telemetry and privacy documentation.

## 4. Level 3: well-governed project

Growing communities may also need:

- governance and maintainer records;
- documented roles, permissions, and decisions;
- public roadmap and deprecation policy;
- succession and continuity plans;
- ownership records for domains, packages, and keys;
- multiple reviewers for sensitive changes;
- release signing or provenance;
- dependency and security policies;
- transparent sustainability practices;
- responsible archive or transfer procedures.

## 5. Project-specific needs

### Small personal project

Prioritize a README, license, short contribution guide, realistic security policy, minimal templates, and an honest maintenance status. Do not invent an organization.

### Library

Document the public API, compatibility, supported versions, examples, versioning, migrations, and reproducible publishing.

### Local application

Document data locations, export, configuration, permissions, updates, telemetry, and file formats.

### Web service

Document architecture, environment variables, infrastructure dependencies, local deployment, backups, migrations, privacy, and the boundary between community code and an operated service.

### AI project

Distinguish code, weights, architecture, training data, training scripts, inference, evaluation, and documentation. Do not call the complete system open source if only one component qualifies.

### Creative project with code

Separate the license for code and tools from terms covering artwork, characters, music, fonts, brands, and other creative assets.

## 6. Review rubric

Score each area from 0 to 3:

- licensing and rights;
- source and reproducibility;
- documentation;
- contributions;
- security;
- privacy and user control;
- interoperability;
- maintenance;
- governance;
- releases.

Interpretation:

- **0:** absent or deceptive;
- **1:** incomplete minimum;
- **2:** adequate;
- **3:** strong and verified.

Never let an average hide blockers. A project without a valid license is not open source even if other areas score highly.

## 7. Primary references

- [GitHub community profiles](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories)
- [OpenSSF Best Practices](https://www.bestpractices.dev/)
- [Semantic Versioning](https://semver.org/)
- [REUSE Specification](https://reuse.software/spec/)
