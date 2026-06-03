# No Secrets in Code

**Statement:** Secrets live in environment variables or secret managers. Never in source code.

**Why:** Committed secrets end up in git history forever, get cloned to every developer's machine, and eventually leak. Rotating a committed secret requires rewriting git history — painful and often incomplete.

## Hard rules

- No API keys, passwords, tokens, or connection strings in source files
- `.env` files are in `.gitignore` — always
- Secrets accessed via environment variables or a secret manager (Vault, AWS SSM, etc.)
- On leak: rotate the secret immediately, then clean the history

## Patterns to watch

These in source code are almost always secrets:

- Strings matching `sk-`, `pk-`, `ghp_`, `gho_`, `AKIA`, `Bearer `
- Variables named `*_KEY`, `*_SECRET`, `*_TOKEN`, `*_PASSWORD`
- Connection strings with credentials (`postgres://user:pass@`)
- Base64 blobs longer than 40 characters
- Hardcoded JWTs

## Soft rules

- Use `.env.example` with placeholder values (never real secrets) for documentation
- Prefer short-lived tokens over long-lived API keys
- Different secrets per environment (dev/staging/prod)

**Enforced by:** `agents/security-reviewer`
