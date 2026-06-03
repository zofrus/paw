# paw hooks

Four hooks. Each fires on a Claude Code lifecycle event. Each testable standalone before wiring.

| Hook | Event | Matcher | What it does |
|---|---|---|---|
| `git_safety.py` | PreToolUse | Bash | Block rebase, force-push, branch -D, reset --hard, checkout . |
| `branch_guard.py` | PreToolUse | Bash | Block commits on main/master/develop/trunk/release |
| `auto_test_detect.sh` | PostToolUse | Write\|Edit | Warn when source file has no corresponding test file |
| `_lib.py` | — | — | Shared helpers (read_payload, emit, find_project_root) |

## Install

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "python3 ~/.paw/hooks/git_safety.py" },
          { "type": "command", "command": "python3 ~/.paw/hooks/branch_guard.py" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "bash ~/.paw/hooks/auto_test_detect.sh" }
        ]
      }
    ]
  }
}
```

## Pipe-testing

Test each hook standalone before wiring:

```bash
# git_safety: should block rebase (exit code 2)
echo '{"tool_input":{"command":"git rebase main"}}' | python3 hooks/git_safety.py
echo "exit=$?"

# git_safety: should block force-push
echo '{"tool_input":{"command":"git push --force origin main"}}' | python3 hooks/git_safety.py

# git_safety: should allow normal push (no output)
echo '{"tool_input":{"command":"git push origin feature/foo"}}' | python3 hooks/git_safety.py

# branch_guard: should block commit on main (run while on main)
echo '{"tool_input":{"command":"git commit -m test"}}' | python3 hooks/branch_guard.py

# auto_test_detect: should warn about missing test
echo '{"tool_input":{"file_path":"src/auth/login.ts"}}' | bash hooks/auto_test_detect.sh
```

## Override env vars

For rare cases where you need to bypass:

| Env var | Overrides |
|---|---|
| `PAW_ALLOW_REBASE=1` | git rebase, git pull --rebase |
| `PAW_ALLOW_FORCE_PUSH=1` | git push --force/--force-with-lease |

No override exists for `branch -D`, `reset --hard`, or `checkout .` — use the safe alternatives.
