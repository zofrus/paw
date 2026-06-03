# Git Safety Skill

**When to use:** Any git operation that could lose work — pull, push, merge, rebase, branch management, conflict resolution.

## Core doctrine

1. **Always pull (merge).** `git pull` defaults to merge. Never use `--rebase`.
2. **Never rebase published history.** Rebase rewrites commits other people have cloned. Use merge.
3. **Never force-push.** `--force` and `--force-with-lease` overwrite remote history. Pull first, then push.
4. **Never commit on main.** Create a feature branch. Always.

## Protected operations and alternatives

| Dangerous | Safe alternative |
|---|---|
| `git rebase main` | `git pull origin main` (merge) |
| `git pull --rebase` | `git pull` (merge) |
| `git push --force` | `git pull origin branch && git push` |
| `git branch -D feature` | `git branch -d feature` (safe delete) |
| `git reset --hard HEAD~1` | `git revert HEAD` or `git stash` |
| `git checkout .` | `git stash` |

## Conflict resolution

When merge conflicts happen:

1. **Understand both sides' intent** — don't blindly pick "ours" or "theirs"
2. **Combine compatible changes** — if both sides add different things, keep both
3. **Escalate competing changes** — if both sides change the same logic differently, get both authors involved
4. **Run tests before committing** the merge resolution
5. **If tests fail after resolution** — escalate, don't guess

## Branch workflow

- One branch per logical task
- Branch names: `feat/description`, `fix/description`, `chore/description`
- Delete branches after merge
- Keep branches short-lived — days, not weeks

## Override escape hatches

For rare cases where you genuinely need the dangerous operation:

| Env var | Overrides |
|---|---|
| `PAW_ALLOW_REBASE=1` | git rebase, git pull --rebase (local unpublished only) |
| `PAW_ALLOW_FORCE_PUSH=1` | git push --force (never to main) |

Set the env var, run the command, unset. You can, but you have to mean it.
