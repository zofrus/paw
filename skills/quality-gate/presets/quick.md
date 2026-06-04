# Quick quality gate

**When to use:** Fast feedback during active development. Catches the obvious stuff.

## Agents

1. `code-reviewer` — correctness, edge cases, naming

## Prompt

```
Use the code-reviewer agent on the current diff.
```

## What it catches

- Logic errors, wrong conditions, missing returns
- Edge cases: null, empty, boundary values
- Error handling gaps (bare catch, swallowed errors)
- Naming that doesn't carry intent

## What it misses

- Latent bug patterns (race conditions, off-by-one) — use `standard`
- Security vulnerabilities — use `standard` or `thorough`
- Performance issues — use `thorough`
