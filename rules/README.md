# paw rules

Six doctrine pages. Source of truth for what agents enforce and hooks block.

| Rule | Enforced by |
|---|---|
| [git-doctrine](git-doctrine.md) | hooks/git_safety.py, hooks/branch_guard.py |
| [test-first](test-first.md) | agents/test-runner, hooks/auto_test_detect.sh |
| [error-handling](error-handling.md) | agents/code-reviewer, agents/bug-auditor |
| [no-secrets-in-code](no-secrets-in-code.md) | agents/security-reviewer |
| [branch-hygiene](branch-hygiene.md) | hooks/branch_guard.py |
| [security-basics](security-basics.md) | agents/security-reviewer |

If a rule contradicts how an agent behaves, fix the agent. Rules are the authority.
