# Architecture Skill

**When to use:** Designing systems, evaluating tradeoffs, deciding component boundaries, planning integration points.

## How to decompose

1. **Identify boundaries** — where does data enter and leave? Each boundary is a potential component edge.
2. **Map data flow** — follow the request from user action to database and back. Every hop is an integration point.
3. **Identify integration points** — external APIs, databases, message queues, file systems. Each is a failure point.
4. **List risks** — what can go wrong at each boundary and integration point?

## When to split vs combine

**Split when:**
- Two things change for different reasons (separate concerns)
- Two things deploy on different schedules
- One thing needs to scale independently

**Combine when:**
- Split would require synchronous communication between the halves
- Both change together almost every time
- The boundary is speculative ("we might need this someday")

## Risk assessment framework

For each risk, assess:

| | Low Impact | High Impact |
|---|---|---|
| **High Likelihood** | Monitor | Mitigate now |
| **Low Likelihood** | Accept | Plan mitigation |

Every risk needs: description, likelihood, impact, and mitigation strategy.

## Presenting alternatives

Always present 2+ approaches:
- **Approach A** — pros, cons, estimated effort, risk profile
- **Approach B** — pros, cons, estimated effort, risk profile
- **Recommendation** — which and why, stated tradeoff

Never present one option as the only option. The point of alternatives is to show you considered the space.
