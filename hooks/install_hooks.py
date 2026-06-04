#!/usr/bin/env python3
"""Install paw hooks into Claude Code settings.json. Called by setup script."""

import json
import os
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: install_hooks.py <paw_dir>", file=sys.stderr)
        sys.exit(1)

    paw_dir = sys.argv[1]
    settings_path = os.path.expanduser("~/.claude/settings.json")

    if os.path.exists(settings_path):
        with open(settings_path) as f:
            try:
                settings = json.load(f)
            except json.JSONDecodeError:
                settings = {}
    else:
        os.makedirs(os.path.dirname(settings_path), exist_ok=True)
        settings = {}

    hooks = settings.setdefault("hooks", {})

    paw_pre = [
        {"type": "command", "command": f"python3 '{paw_dir}/hooks/git_safety.py'"},
        {"type": "command", "command": f"python3 '{paw_dir}/hooks/branch_guard.py'"},
    ]
    paw_post = [
        {"type": "command", "command": f"bash '{paw_dir}/hooks/auto_test_detect.sh'"},
    ]

    paw_cmds = {h["command"] for h in paw_pre + paw_post}
    existing_cmds = set()
    for entry in hooks.get("PreToolUse", []) + hooks.get("PostToolUse", []):
        for h in entry.get("hooks", []):
            existing_cmds.add(h.get("command", ""))

    if paw_cmds & existing_cmds:
        print("  paw hooks already installed in settings.json.")
        return

    pre_entries = hooks.get("PreToolUse", [])
    post_entries = hooks.get("PostToolUse", [])

    pre_entries.append({"matcher": "Bash", "hooks": paw_pre})
    post_entries.append({"matcher": "Write|Edit", "hooks": paw_post})

    hooks["PreToolUse"] = pre_entries
    hooks["PostToolUse"] = post_entries

    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)
        f.write("\n")

    print("  Hooks installed successfully.")


if __name__ == "__main__":
    main()
