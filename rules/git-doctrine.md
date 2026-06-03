# Git Doctrine

**Statement:** Always `git pull` (merge). Never rebase published history. Never force-push.

**Why:** Rebase rewrites commit history, breaking other clones that reference those commits. Force-push overwrites remote work. Both are theoretically recoverable but practically disastrous. Merge commits are cheap. Lost work is expensive.

## Hard rules

- `git pull` always uses merge, never `--rebase`
- `git rebase` against any published ref is blocked (override: `PAW_ALLOW_REBASE=1` for unpublished local only)
- `git push --force` / `-f` / `--force-with-lease` is blocked (override: `PAW_ALLOW_FORCE_PUSH=1`, never to main)
- `git branch -D` is blocked — use `git branch -d` (safe delete)
- `git reset --hard` is blocked — use `git stash` or `git revert`
- `git checkout .` is blocked — use `git stash`

## Soft rules

- Before push: `git pull` to integrate, resolve conflicts, then push
- Prefer many small commits over squashed (keeps bisect useful)
- Commit messages: imperative mood, 72 chars max first line

## How to apply

| Situation | Wrong | Right |
|---|---|---|
| Update branch with main | `git rebase main` | `git pull origin main` |
| Push rejected | `git push --force` | `git pull origin branch && git push` |
| Remove a commit | `git reset --hard HEAD~1` | `git revert HEAD` |
| Clean old branch | `git branch -D old-branch` | `git branch -d old-branch` |

**Enforced by:** `hooks/git_safety.py`, `hooks/branch_guard.py`
