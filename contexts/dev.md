# Dev Context

**Posture:** Smallest change that works. Tests first or alongside. One commit per logical step. Read before write.

## Key questions

- What does the acceptance criterion say?
- What test proves it's met?
- What's the smallest change to pass the test?
- What existing code overlaps with this change?
- What's the rollback plan?

## What to avoid

- Features the spec doesn't ask for
- Refactoring unrelated code in the same branch
- Error handling for impossible scenarios
- Feature flags when you can just change the code
- Comments that narrate what the code does (names should do that)
- Premature abstraction — three similar lines is better than a wrong abstraction

## When to escalate

- Spec is ambiguous — ask before guessing
- Acceptance criterion can't be met without breaking existing behavior
- Change requires a database migration
- Change touches authentication, authorization, or PII

## Done means

- Tests pass locally
- New tests exist alongside new code
- Commits are logical steps with imperative messages (72 char first line)
- Branch is ready for review
