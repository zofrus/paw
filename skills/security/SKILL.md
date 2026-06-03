# Security Skill

**When to use:** Any code touching authentication, user input, external APIs, or sensitive data.

## OWASP Top 10 cheat sheet

| # | Category | One-line check |
|---|---|---|
| A01 | Broken access control | Is authz checked at the endpoint boundary, not just the UI? |
| A02 | Crypto failures | Any weak algorithms (MD5, SHA1 for passwords)? Plaintext sensitive data? |
| A03 | Injection | Is every query parameterized? Any string interpolation into SQL/commands? |
| A04 | Insecure design | Was there a threat model? Or just hoping for the best? |
| A05 | Misconfiguration | Debug mode off in prod? Default credentials removed? CORS restrictive? |
| A06 | Vulnerable components | Dependencies audited for CVEs? |
| A07 | Auth failures | Session fixation possible? Password policy enforced? |
| A08 | Data integrity | Updates signed? CI inputs trusted? |
| A09 | Logging failures | Security events logged? PII NOT logged? |
| A10 | SSRF | Outbound requests validated? DNS rebinding mitigated? |

## Input validation patterns

- Validate at the boundary — first point where external data enters your system
- Check: type, length, format, range, encoding
- Reject early — don't process invalid input hoping it works out
- Prefer allowlists (define what's valid) over denylists (define what's invalid)

## Output encoding

Context-dependent — there is no universal "escape":

| Context | Encoding |
|---|---|
| HTML body | HTML entity encode (`&lt;`, `&gt;`, `&amp;`) |
| HTML attribute | Attribute encode + quote the attribute |
| JavaScript | JS string encode, or use JSON.stringify |
| SQL | Parameterized queries (not escaping) |
| URL | URL encode (`encodeURIComponent`) |

## Secret management

- Environment variables or secret manager (Vault, AWS SSM, GCP Secret Manager)
- Never in source code, never in git history
- Rotate immediately on any leak — investigate after
- Different secrets per environment
- Short-lived tokens preferred over long-lived API keys

## PII handling

- Redact in logs (emails, names, addresses, phone numbers, SSNs)
- Encrypt at rest in databases
- Minimize collection — don't store what you don't need
- Audit access — who can query PII and when

## Prompt injection defense

If your code integrates with LLMs:

- User input is **data**, not **instructions** — never interpolate it into system prompts
- Separate system instructions from user content with clear delimiters
- Validate LLM output before acting on it (especially tool calls)
- Log LLM interactions for forensic reconstruction
