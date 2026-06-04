"""Tests for hooks/branch_guard.py."""

import json
import subprocess
import sys

HOOK = "hooks/branch_guard.py"


def run_hook(command):
    payload = json.dumps({"tool_input": {"command": command}})
    result = subprocess.run(
        [sys.executable, HOOK],
        input=payload,
        capture_output=True,
        text=True,
        timeout=10,
    )
    return result


def test_allows_non_commit():
    r = run_hook("git push origin main")
    assert r.returncode == 0


def test_allows_commit_on_feature_branch():
    """This test only passes if we're not currently on a protected branch."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
    )
    branch = result.stdout.strip()
    if branch in {"main", "master", "develop", "trunk", "release"}:
        return  # skip — can't test "allow" while on protected branch
    r = run_hook("git commit -m 'test'")
    assert r.returncode == 0


def test_blocks_on_protected_branch_when_applicable():
    """If we're on main, verify it blocks."""
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
    )
    branch = result.stdout.strip()
    if branch not in {"main", "master", "develop", "trunk", "release"}:
        return  # skip — not on protected branch
    r = run_hook("git commit -m 'test'")
    assert r.returncode == 2
    out = json.loads(r.stdout)
    assert "block" in out["hookSpecificOutput"]["permissionDecision"]


def test_malformed_json():
    result = subprocess.run(
        [sys.executable, HOOK],
        input="not json",
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0


def test_empty_command():
    r = run_hook("")
    assert r.returncode == 0
