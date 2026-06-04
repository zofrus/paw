# Standard quality gate

**When to use:** Before requesting code review. The default for most PRs.

## Agents

1. `code-reviewer` — correctness, edge cases, naming
2. `bug-auditor` — race conditions, off-by-one, null deref, encoding
3. `security-reviewer` — OWASP Top 10, injection, auth, secrets

## Prompt

```
Use the code-reviewer agent, then the bug-auditor agent,
then the security-reviewer agent on the current diff.
```

## What it catches

Everything in `quick`, plus:
- Latent bug patterns with concrete reproduction scenarios
- SQL injection, XSS, SSRF, broken auth, hardcoded secrets
- OWASP Top 10 coverage

## What it misses

- Performance at scale — use `thorough`
- Frontend-specific issues — add `fe-reviewer`
- PHP/Laravel-specific issues — add `php-reviewer`
- Documentation gaps — use `thorough`
