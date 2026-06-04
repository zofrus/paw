"""Tests for hooks/git_safety.py — the most security-critical hook."""

import json
import subprocess
import sys

HOOK = "hooks/git_safety.py"


def run_hook(command, env=None):
    payload = json.dumps({"tool_input": {"command": command}})
    result = subprocess.run(
        [sys.executable, HOOK],
        input=payload,
        capture_output=True,
        text=True,
        timeout=5,
        env=env,
    )
    return result


def parse_output(result):
    if not result.stdout.strip():
        return None
    return json.loads(result.stdout)


# ── Blocking tests ────────────────────────────────────


def test_blocks_rebase():
    r = run_hook("git rebase main")
    assert r.returncode == 2
    out = parse_output(r)
    assert out["hookSpecificOutput"]["permissionDecision"] == "block"


def test_blocks_pull_rebase():
    r = run_hook("git pull --rebase origin main")
    assert r.returncode == 2


def test_blocks_force_push():
    r = run_hook("git push --force origin main")
    assert r.returncode == 2


def test_blocks_force_push_short():
    r = run_hook("git push -f origin main")
    assert r.returncode == 2


def test_blocks_branch_delete():
    r = run_hook("git branch -D feature")
    assert r.returncode == 2


def test_blocks_reset_hard():
    r = run_hook("git reset --hard HEAD~1")
    assert r.returncode == 2


def test_blocks_checkout_dot():
    r = run_hook("git checkout .")
    assert r.returncode == 2


def test_blocks_checkout_dot_chained():
    r = run_hook("git checkout . && echo done")
    assert r.returncode == 2


# ── Allow tests ───────────────────────────────────────


def test_allows_normal_push():
    r = run_hook("git push origin feature/foo")
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_allows_force_with_lease():
    r = run_hook("git push --force-with-lease origin feature/foo")
    assert r.returncode == 0
    assert r.stdout.strip() == ""


def test_allows_normal_pull():
    r = run_hook("git pull origin main")
    assert r.returncode == 0


def test_allows_branch_safe_delete():
    r = run_hook("git branch -d feature")
    assert r.returncode == 0


def test_allows_normal_checkout():
    r = run_hook("git checkout feature/foo")
    assert r.returncode == 0


def test_allows_empty_command():
    r = run_hook("")
    assert r.returncode == 0


def test_allows_non_git():
    r = run_hook("npm install")
    assert r.returncode == 0


# ── Bypass prevention ─────────────────────────────────


def test_multiline_bypass_blocked():
    r = run_hook("echo skip &&\ngit push --force")
    assert r.returncode == 2


def test_multiline_rebase_blocked():
    r = run_hook("cd /tmp &&\ngit rebase main")
    assert r.returncode == 2


# ── Malformed input ───────────────────────────────────


def test_malformed_json():
    result = subprocess.run(
        [sys.executable, HOOK],
        input="not json",
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert result.returncode == 0


def test_empty_stdin():
    result = subprocess.run(
        [sys.executable, HOOK],
        input="",
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert result.returncode == 0


def test_missing_tool_input():
    result = subprocess.run(
        [sys.executable, HOOK],
        input=json.dumps({"other": "data"}),
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert result.returncode == 0
