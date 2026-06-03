# Review Context

**Posture:** Read carefully — two passes. First for sense-check, second for what-could-break. Assume nothing. Be specific. Distinguish severity.

## Key questions

- **Correctness** — does it do what the spec says?
- **Edge cases** — empty, null, max, concurrent?
- **Concurrency** — shared state, async correctness, race conditions?
- **Error paths** — are failures logged and handled, or swallowed?
- **Tests** — do they exist, exercise behavior, cover unhappy paths?
- **Observability** — are there logs at boundaries, metrics for SLIs?
- **Security** — input validated, output encoded, authz checked?

## What NOT to flag

- ESLint / formatter nits (the formatter handles those)
- Reasonable naming differences that are preference, not clarity
- Architectural rewrites on already-merged code
- Missing features the spec doesn't require

## Severity levels

- **Critical** — blocks merge (data loss, security, crash, undocumented breaking change)
- **Warning** — fix before merge (missing test, swallowed error, unclear public API)
- **Info** — optional (nit, minor improvement)

## When to escalate

- You reviewed your own code — request a fresh reviewer
- Change is security-sensitive — ensure security-reviewer also runs
- You don't understand a pattern — ask the author, don't guess

## Done means

Every changed file got two passes. Every finding is specific, actionable, and honestly severity-calibrated.
