"""Tests for hooks/_lib.py."""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "hooks"))

from _lib import emit, find_project_root  # noqa: E402


def test_emit_block(capsys):
    emit("bad command", "block", "not allowed")
    out = json.loads(capsys.readouterr().out)
    assert out["systemMessage"] == "bad command"
    assert out["hookSpecificOutput"]["permissionDecision"] == "block"
    assert out["hookSpecificOutput"]["reason"] == "not allowed"


def test_emit_allow_with_message(capsys):
    emit("just info")
    out = json.loads(capsys.readouterr().out)
    assert out["systemMessage"] == "just info"
    assert "hookSpecificOutput" not in out


def test_emit_empty_is_silent(capsys):
    emit()
    assert capsys.readouterr().out == ""


def test_emit_allow_no_message_is_silent(capsys):
    emit("")
    assert capsys.readouterr().out == ""


def test_find_project_root_finds_this_repo():
    root = find_project_root(os.path.dirname(__file__))
    assert root is not None
    assert os.path.exists(os.path.join(root, "pyproject.toml"))


def test_find_project_root_returns_none_at_fs_root():
    result = find_project_root("/")
    assert result is None


def test_find_project_root_depth_cap():
    result = find_project_root("/nonexistent/deep/path/that/goes/nowhere")
    assert result is None
