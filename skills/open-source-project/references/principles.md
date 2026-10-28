# Principles for evaluating practical openness

## Contents

1. Minimum freedoms
2. Open source and free software
3. Open-washing
4. User autonomy
5. Interoperability and portability
6. Privacy and telemetry
7. Community and authority
8. Primary references

## 1. Minimum freedoms

A genuinely open project must allow people to:

- use the software for any purpose;
- study how it works;
- modify it;
- share original or modified copies.

Source access is necessary but insufficient. The published source must be the preferred form for modification, and the license must permit people to exercise these freedoms.

## 2. Open source and free software

The terms overlap but reflect different traditions:

- **Open source** usually emphasizes licensing criteria, collaboration, and development methodology.
- **Free software** emphasizes the freedoms and rights of software users.

Use insights from both traditions without hiding their differences or treating either term as a synonym for “free of charge.”

## 3. Open-washing

Look for:

- a public repository with no license;
- a non-commercial or no-competition license marketed as open source;
- an open SDK or interface while the essential component remains closed;
- source that is older than the distributed product;
- builds that require undisclosed private tools or keys;
- missing models, datasets, or assets required to run the project;
- “community governance” without meaningful authority outside the owner;
- intentionally limited data export;
- undisclosed telemetry;
- security or quality badges unsupported by real verification.

Describe the project precisely: source-available, open client with a closed server, open core with proprietary services, open-weight model, or another accurate term.

## 4. User autonomy

Evaluate whether people can reasonably:

- run the software locally;
- understand its behavior;
- configure it without patching source;
- retain and export their data;
- migrate to another tool;
- disable external services and telemetry;
- repair and extend the system;
- maintain a fork if the original project changes direction.

Not every project must be local-first, but dependencies that concentrate control must be visible.

## 5. Interoperability and portability

Favor documented or open formats, documented APIs, import and export, portable configuration, alternative implementations, separation between core logic and provider-specific infrastructure, deterministic build instructions, and explicit data migrations.

## 6. Privacy and telemetry

Document:

- data collected;
- purpose and destination;
- retention;
- third parties;
- opt-out controls;
- default behavior;
- outbound connections.

A public repository alone does not make a project privacy-first.

## 7. Community and authority

Transparency includes acknowledging who decides. A project can be genuinely open while led by one maintainer, a company, a foundation, or a benevolent dictator. The problem is concealed authority or symbolic participation presented as community power.

Document maintainers, contribution scope, review process, reserved decisions, conflict resolution, succession, and ownership of domains, trademarks, packages, and release keys.

## 8. Primary references

- [Open Source Definition](https://opensource.org/osd)
- [OSI-approved licenses](https://opensource.org/licenses)
- [Free Software Definition](https://www.gnu.org/philosophy/free-sw.html)
- [Open Source AI Definition](https://opensource.org/ai/open-source-ai-definition)
