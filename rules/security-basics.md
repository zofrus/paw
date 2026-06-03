# Security Basics

**Statement:** Validate input at boundaries. Encode output for context. Least privilege. Defense in depth.

**Why:** Most vulnerabilities come from trusting data that crossed a trust boundary. Input validation and output encoding eliminate entire classes of attacks. Least privilege limits blast radius when something does go wrong.

## Hard rules

- All user input validated before use (type, length, format, range)
- Output encoded for its context (HTML, SQL, JS, URL — each different)
- Auth checked at every endpoint — not just the controller, the route middleware too
- Secrets never logged, even at debug level
- Dependencies audited for known CVEs before adding

## Soft rules

- Prefer allowlists over denylists (define what's valid, reject everything else)
- Fail closed, not open — if the auth check errors, deny access
- Log security-relevant events (login attempts, permission changes, admin actions)
- Rate limit authentication endpoints
- Use parameterized queries exclusively — never string-interpolate SQL

## How to apply

| Wrong | Right |
|---|---|
| `db.query("SELECT * FROM users WHERE id=" + id)` | `db.query("SELECT * FROM users WHERE id=$1", [id])` |
| `res.send("<h1>" + userName + "</h1>")` | `res.send("<h1>" + escapeHtml(userName) + "</h1>")` |
| Auth check in controller only | Auth middleware on the route group |
| `console.log("Login:", { email, password })` | `console.log("Login attempt:", { email })` |

**Enforced by:** `agents/security-reviewer`
