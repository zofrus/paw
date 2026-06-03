# Error Handling

**Statement:** No silent failures. Catch + log + escalate or re-throw. Never swallow.

**Why:** `try/except/pass` and `try { } catch (e) {}` are the most expensive lines ever written. They turn observable failures into invisible bugs that surface days later as data corruption with no trail.

## Hard rules

- Every `try` block has a logged catch path — bare `catch {}` is forbidden
- Catches that genuinely absorb errors must explain why in a comment
- Errors crossing module boundaries are typed — don't `throw "string"`
- Network/IO/external calls have retry with backoff and a max attempts cap
- Errors affecting data integrity halt the operation — never continue with bad data

## Soft rules

- Prefer `Result<T,E>` / Either over throw at API boundaries (failure is explicit in the type)
- Include the input that produced the error in the log (after PII redaction)
- Distinguish expected errors (rate limit, 404) from unexpected (NPE, type error) via log levels

## How to apply

| Wrong | Right |
|---|---|
| `try { ... } catch (e) {}` | `try { ... } catch (e) { logger.error('context', e); throw; }` |
| `except Exception: pass` | `except SpecificError as e: logger.warning(f"...: {e}")` |
| `throw "something went wrong"` | `throw new ValidationError("email format invalid", { input })` |

**Enforced by:** `agents/code-reviewer`, `agents/bug-auditor`
