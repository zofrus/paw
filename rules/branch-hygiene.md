# Branch Hygiene

**Statement:** Feature branch per task. Never commit directly to main.

**Why:** Direct commits to main bypass review, break CI for everyone, and make rollback painful. Feature branches isolate changes, enable review, and keep main always deployable.

## Hard rules

- Never commit to `main`, `master`, `develop`, `trunk`, or `release` directly
- One branch per logical task — don't mix unrelated changes
- Branch names follow: `type/description` (e.g., `feat/password-reset`, `fix/null-deref-login`, `chore/update-deps`)
- Delete branches after merge

## Soft rules

- Keep branches short-lived — merge within days, not weeks
- Pull main into your branch regularly (merge, not rebase) to stay current
- Prefix types: `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`, `test/`

## How to apply

| Wrong | Right |
|---|---|
| `git commit -m "fix" (on main)` | `git checkout -b fix/login-null-check && git commit -m "fix"` |
| One branch with 5 unrelated changes | 5 branches, each with one concern |
| Branch open for 3 weeks | Merge or split within a few days |

**Enforced by:** `hooks/branch_guard.py`
