# Thorough quality gate

**When to use:** Before merging significant features, after refactors, or on security-sensitive code.

## Agents

1. `code-reviewer` — correctness, edge cases, naming
2. `bug-auditor` — race conditions, off-by-one, null deref, encoding
3. `security-reviewer` — OWASP Top 10, injection, auth, secrets
4. `perf-checker` — N+1 queries, unbounded fetches, missing pagination
5. `test-runner` — run test suite, surface failures and gaps
6. `docs-writer` — flag stale or missing documentation
7. `fe-reviewer` (if frontend code changed)
8. `php-reviewer` (if PHP code changed)

## Prompt

```
Use the code-reviewer, bug-auditor, security-reviewer,
perf-checker, test-runner, and docs-writer agents on
the current diff.
```

Add `fe-reviewer` and/or `php-reviewer` if relevant code changed.

## What it catches

Everything in `standard`, plus:
- N+1 queries, full-table scans, missing pagination
- Test coverage gaps on changed code
- Stale README, missing CHANGELOG entries, undocumented public API
- Accessibility issues, component structure, hooks misuse (frontend)
- Eloquent N+1, mass assignment, CSRF gaps (PHP)
