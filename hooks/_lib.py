#!/usr/bin/env python3
"""paw hook helpers."""

import json
import os
import sys

MAX_TRAVERSAL_DEPTH = 50


def read_payload():
    try:
        return json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        print("paw: malformed JSON on stdin", file=sys.stderr)
        return {}
    except (EOFError, IOError):
        return {}


def emit(message="", decision="allow", reason=""):
    output = {}
    if message:
        output["systemMessage"] = message
    if decision != "allow":
        output["hookSpecificOutput"] = {
            "permissionDecision": decision,
            "reason": reason,
        }
    if output:
        print(json.dumps(output))


def find_project_root(start=None):
    d = start or os.getcwd()
    markers = [
        "package.json",
        "pyproject.toml",
        "go.mod",
        "composer.json",
        "Cargo.toml",
    ]
    for _ in range(MAX_TRAVERSAL_DEPTH):
        if any(os.path.exists(os.path.join(d, m)) for m in markers):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent
    return None
