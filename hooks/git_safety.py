#!/usr/bin/env python3
"""Block dangerous git operations. PreToolUse hook, matcher: Bash."""

import re
import os
import sys

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
    # --force and -f are blocked. --force-with-lease is intentionally ALLOWED.
    #
    # For 99% of workflows, just pulling first is the right move — and that's
    # what paw's git doctrine enforces. --force-with-lease exists for the 1%
    # case where you can't pull because the history has intentionally diverged.
    #
    # The real scenario: you rebased a local branch (rewriting commits), or you
    # amended a commit you already pushed to a feature branch. Now your local
    # and remote histories are incompatible — git pull would create a merge
    # conflict with yourself. A regular git push is rejected. You need to
    # overwrite the remote, but you want to make sure nobody else pushed to
    # that branch while you weren't looking.
    #
    # --force-with-lease refuses to push if the remote has changed since your
    # last fetch. It's a force push with a safety check. That's the only
    # legitimate use. paw allows it but doesn't encourage it — if you follow
    # paw's "never rebase published history" rule, you'll never need it.
    (
        r"\bgit\s+push\s+.*(-f\b|--force(?!-with-lease)\b)",
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
        r"\bgit\s+checkout\s+\.",
        None,
        "git checkout . silently discards all changes. Use 'git stash' instead.",
    ),
]


def normalize_command(cmd):
    """Flatten multi-line commands so regex patterns can't be bypassed via newlines."""
    return " ".join(cmd.split())


def main():
    payload = read_payload()
    cmd = payload.get("tool_input", {}).get("command", "")
    if not cmd:
        return

    cmd = normalize_command(cmd)

    for pattern, override_env, reason in BLOCKS:
        if re.search(pattern, cmd):
            if override_env and os.environ.get(override_env) == "1":
                continue
            emit(reason, "block", reason)
            sys.exit(2)


if __name__ == "__main__":
    main()
