# Quality Gate Skill

**When to use:** Reviewing code before merge. Running multiple review agents. Deciding what blocks and what doesn't.

## The review checklist

Run through these dimensions for every change:

| Dimension | What to check |
|---|---|
| **Correctness** | Does it do what the spec says? Not what you assume it should do. |
| **Edge cases** | Empty input, null, max values, concurrent access, unicode, timezone |
| **Error handling** | Are failures logged and handled? Or swallowed silently? |
| **Tests** | Do they exist? Exercise behavior (not just import)? Cover unhappy paths? |
| **Observability** | Logs at boundaries? Metrics for SLIs? Enough to debug at 3 AM? |
| **Security** | Input validated? Output encoded? Authz checked? Secrets safe? |
| **Documentation** | Public API documented? Breaking changes noted? CHANGELOG updated? |
| **Performance** | N+1 queries? Unbounded fetches? Missing pagination? |

## Severity rubric

Not everything is critical. Honest severity is more useful than inflated severity.

| Level | Meaning | Action |
|---|---|---|
| **Critical** | Data loss, security vulnerability, runtime crash, undocumented breaking change | Blocks merge. Must fix. |
| **Warning** | Missing test, swallowed error, unclear naming on public API, missing docs | Fix before merge. |
| **Info** | Nit, style preference, optional improvement, minor inconsistency | Optional. Author decides. |

## Running multiple reviewers

Invoke each agent by name. They work independently — that's the point.

```
> Use the code-reviewer agent on the current diff.
> Use the bug-auditor agent on the current diff.
> Use the security-reviewer agent on the current diff.
```

Each checks different dimensions. Aggregate findings by severity:
- Any **critical** from any agent = do not merge
- **Warnings** = fix before merge
- **Info** = author decides

## What NOT to flag in reviews

- Formatter / linter issues (the formatter handles those)
- Style preferences that are opinion, not clarity
- Architectural rewrites of already-merged code
- Missing features the spec doesn't require
