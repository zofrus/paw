#!/usr/bin/env python3
"""Block commits on protected branches. PreToolUse hook, matcher: Bash."""
import re, subprocess, sys, os

sys.path.insert(0, os.path.dirname(__file__))
from _lib import read_payload, emit

PROTECTED = {"main", "master", "develop", "trunk", "release"}


def current_branch():
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def main():
    payload = read_payload()
    cmd = payload.get("tool_input", {}).get("command", "")

    if not re.search(r"\bgit\s+commit\b", cmd):
        return

    branch = current_branch()
    if branch and branch in PROTECTED:
        reason = f"Cannot commit directly to '{branch}'. Create a feature branch first."
        emit(reason, "block", reason)
        sys.exit(2)


if __name__ == "__main__":
    main()
