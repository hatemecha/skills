# Skills de Ingeniería de Software

[English](README.md) · [Español](README.es.md)

Una colección de [Agent Skills](https://agentskills.io/specification) reutilizables para el desarrollo de software. Cada skill ofrece instrucciones prácticas para una tarea concreta, desde diseñar una funcionalidad hasta depurar errores o revisar código.

Pensadas para agentes de programación compatibles, como Codex, Cursor y OpenCode.

## Instalación

```bash
npx skills add hatemecha/skills
```

Para tenerlas disponibles en todos tus proyectos, agregá `-g`:

```bash
npx skills add hatemecha/skills -g
```

También podés [explorar la colección en skills.sh](https://skills.sh/hatemecha/skills).

## Skills

### Ingeniería

| Skill | Para qué sirve |
| --- | --- |
| [Engineering Workflow](skills/engineering-workflow/SKILL.md) | Elige un enfoque de trabajo y las skills pertinentes sin agregar procesos innecesarios. |
| [Open Source Engineering](skills/open-source-engineering/SKILL.md) | Orienta la implementación, refactorización y revisión de código hacia soluciones claras y mantenibles. |
| [Systematic Debugging](skills/systematic-debugging/SKILL.md) | Investiga fallos mediante reproducción, evidencia y análisis de sus causas. |
| [Test Strategy](skills/test-strategy/SKILL.md) | Selecciona pruebas y verificaciones útiles según los cambios y sus riesgos. |

### Diseño y coordinación

| Skill | Para qué sirve |
| --- | --- |
| [Engineering Brainstorming](skills/engineering-brainstorming/SKILL.md) | Convierte requisitos poco claros en un diseño acotado y listo para implementar. |
| [Orchestrating Engineering Agents](skills/orchestrating-engineering-agents/SKILL.md) | Coordina agentes independientes y revisiones basadas en evidencia cuando la tarea lo justifica. |
| [Context Handoff](skills/context-handoff/SKILL.md) | Transfiere decisiones, avances y resultados verificados entre agentes o sesiones. |

### Código abierto

| Skill | Para qué sirve |
| --- | --- |
| [Open Source Project](skills/open-source-project/SKILL.md) | Revisa licencias, documentación y preparación para publicar un proyecto. |

## Uso

Podés pedirle a tu agente que utilice una skill por su nombre. Por ejemplo:

> Usá `systematic-debugging` para investigar esta regresión.

Para tareas más amplias, empezá con `engineering-workflow`, que ayuda a identificar las skills necesarias. El descubrimiento y la activación automática dependen de cada agente.

## Contribuciones

Se aceptan propuestas de mejora y reportes de errores concretos. Consultá [Contributing](CONTRIBUTING.md).

## Licencia

[MIT](LICENSE).
