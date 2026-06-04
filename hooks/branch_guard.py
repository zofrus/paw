#!/usr/bin/env python3
"""Block commits on protected branches. PreToolUse hook, matcher: Bash."""

import re
import subprocess
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _lib import read_payload, emit

PROTECTED = {"main", "master", "develop", "trunk", "release"}


def parse_git_cwd(cmd):
    """Extract -C <dir> from a git command, if present."""
    match = re.search(r"\bgit\s+-C\s+(\S+)", cmd)
    return match.group(1) if match else None


def current_branch(cwd=None):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=cwd,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def main():
    payload = read_payload()
    cmd = payload.get("tool_input", {}).get("command", "")

    if not re.search(r"\bgit\s+commit\b", cmd):
        return

    git_cwd = parse_git_cwd(cmd)
    branch = current_branch(cwd=git_cwd)
    if branch is None:
        emit(
            "Could not determine current branch. Commit blocked as a precaution.",
            "block",
            "Branch detection failed — fail-closed.",
        )
        sys.exit(2)

    if branch in PROTECTED:
        reason = f"Cannot commit directly to '{branch}'. Create a feature branch first."
        emit(reason, "block", reason)
        sys.exit(2)


if __name__ == "__main__":
    main()
