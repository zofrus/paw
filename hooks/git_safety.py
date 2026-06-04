#!/usr/bin/env python3
"""Block dangerous git operations. PreToolUse hook, matcher: Bash."""

import re
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _lib import read_payload, emit

BLOCKS = [
    (
        r"\bgit\s+rebase\b",
        "PAW_ALLOW_REBASE",
        "git rebase rewrites published history. Use 'git pull origin <branch>' instead.",
    ),
    (
        r"\bgit\s+pull\s+.*--rebase\b",
        "PAW_ALLOW_REBASE",
        "git pull --rebase rewrites history. Use 'git pull' (merge) instead.",
    ),
    (
        r"\bgit\s+push\s+.*(-f\b|--force\b|--force-with-lease\b)",
        "PAW_ALLOW_FORCE_PUSH",
        "Force-push overwrites remote history. Use 'git pull' then 'git push' instead.",
    ),
    (
        r"\bgit\s+branch\s+-D\b",
        None,
        "git branch -D force-deletes. Use 'git branch -d' (safe delete) instead.",
    ),
    (
        r"\bgit\s+reset\s+--hard\b",
        None,
        "git reset --hard discards uncommitted work. Use 'git stash' instead.",
    ),
    (
        r"\bgit\s+checkout\s+\.\s*$",
        None,
        "git checkout . silently discards all changes. Use 'git stash' instead.",
    ),
]


def main():
    payload = read_payload()
    cmd = payload.get("tool_input", {}).get("command", "")
    if not cmd:
        return

    for pattern, override_env, reason in BLOCKS:
        if re.search(pattern, cmd):
            if override_env and os.environ.get(override_env) == "1":
                continue
            emit(reason, "block", reason)
            sys.exit(2)


if __name__ == "__main__":
    main()
