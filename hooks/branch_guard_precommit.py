#!/usr/bin/env python3
"""Native git pre-commit hook version of branch_guard.
Works with the pre-commit framework (https://pre-commit.com).
Does not require Claude Code — runs as a standard git hook.
"""

import subprocess
import sys

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
    branch = current_branch()
    if branch and branch in PROTECTED:
        print(f"paw: cannot commit directly to '{branch}'.")
        print("Create a feature branch first:")
        print("  git checkout -b feat/your-change")
        sys.exit(1)


if __name__ == "__main__":
    main()
