# buggy-app — a practice target for paw agents

This app has intentional bugs, security holes, missing tests, and code smells. Use it to see what paw's review agents catch.

## How to use

```
> Use the code-reviewer agent on examples/buggy-app/
> Use the bug-auditor agent on examples/buggy-app/
> Use the security-reviewer agent on examples/buggy-app/
```

Or use the paw CLI:

```
paw check
```

## What's wrong with it

Don't read this until after you've run the agents — see if they find everything.

<details>
<summary>Spoilers (click to reveal)</summary>

### Security
- `app.py:8` — hardcoded JWT secret
- `app.py:23` — SQL injection via string interpolation
- `app.py:34` — password logged in plaintext
- `app.py:42` — no rate limiting on login
- `app.py:48` — no CSRF protection
- `app.py:15` — API key in source code

### Bugs
- `app.py:23` — SQL injection is also a correctness bug (breaks on names with quotes)
- `app.py:56` — off-by-one in pagination (skips first result)
- `app.py:62` — race condition on counter increment (no lock)
- `app.py:70` — bare except swallows all errors silently
- `app.py:75` — N+1 query in loop

### Missing
- Zero test files
- No input validation
- No error handling on database connection
- No documentation

</details>
