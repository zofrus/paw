# Security Context

**Posture:** Threat-model first. Trust nothing from outside the trust boundary. Least privilege. Defense in depth.

## Key questions

- **Authentication** — who is this? How do we verify? Token lifetime? Rotation?
- **Authorization** — what are they allowed to do? Permission checked at the boundary?
- **Input validation** — type, length, format, range, encoding? Reject early?
- **Output encoding** — contextually encoded at every boundary (HTML, SQL, JS, URL)?
- **Secrets** — where stored? Who can read? Rotation policy?
- **PII** — in logs? In metrics? In backups? Redacted?
- **Dependencies** — known CVEs? Supply chain risk?
- **Logging** — can we detect an attack? Reconstruct what happened forensically?
- **Prompt injection** — if LLM-integrated, is user input treated as data, not instructions?

## What to avoid

- "Nobody would think to do that" — they will
- "We'll fix it later" — you won't
- Security through obscurity as the only layer
- Adding features to security tooling in the same PR

## When to escalate

- Active exploit in progress — switch to incident context
- Team can't fix within a reasonable window — notify leadership
- Customer data exposure — legal and comms immediately
- Leaked credential — rotate first, investigate second

## Done means

Findings documented with severity and reproduction steps. Fixes have tests that fail on the vulnerable version. Leaked credentials rotated. Post-mortem captures prevention measures.
