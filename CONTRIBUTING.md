# Contributing to paw

Contributions are welcome! paw is an open-source project and we appreciate help from the community.

## Before you start

- **All PRs require maintainer approval** before merging. This is enforced by branch protection.
- Open an issue first for large changes (new agents, new skills, architectural changes) so we can discuss the approach.
- Small fixes (typos, bug fixes, test additions) can go straight to a PR.

## Quick version

1. Fork the repo
2. Clone your fork and set up the dev environment
3. Create a feature branch (`feat/your-change`)
4. Write tests for your change
5. Run the full test suite (see below)
6. Submit a PR

## Development setup

```bash
git clone https://github.com/YOUR-USERNAME/paw.git ~/paw
cd ~/paw
./paw setup

# Verify everything works
python3 -m pytest tests/ -v
ruff check .
ruff format --check .
```

Requirements:
- Python 3.10+
- git
- A terminal with curses support (standard on macOS/Linux)

## What to contribute

- **New agents** — follow the pattern in `agents/architect.md`. Pick a context, pick rules, define minimum tools.
- **New rules** — follow the pattern in `rules/git-doctrine.md`. Statement, why, hard rules, soft rules, enforced by.
- **New skills** — create `skills/your-skill/SKILL.md` with domain knowledge.
- **Bug fixes** — especially in hooks (security-critical code).
- **Tutorial improvements** — edit `tutorial_engine/content.py` for content, `tutorial_engine/engine.py` for rendering.
- **Tests** — more coverage is always welcome, especially for edge cases in hooks.

## Required checks before submitting a PR

Every PR must pass these checks. Run them locally before pushing:

```bash
# Run the full test suite (64 tests)
python3 -m pytest tests/ -v

# Lint — must have zero errors
ruff check .

# Format — must match ruff's formatting
ruff format --check .
```

If `ruff format --check` fails, auto-fix with:

```bash
ruff format .
```

## Rules

- **Tests before code.** The `test-first` rule applies to paw itself. If you're adding functionality, add tests first.
- **No secrets in code.** No API keys, tokens, or credentials — ever.
- **Feature branch per change.** Never commit to main directly.
- **Hooks are security-critical.** Changes to `hooks/` require corresponding tests in `tests/`.
- **Agents are least-privilege.** New agents should request the minimum tools needed. Default to read-only.

## Style

- **Python:** ruff format + ruff check (no config needed, defaults are fine)
- **Markdown:** no linter, just be consistent with existing files
- **Commits:** imperative mood, short first line, explain the why

## PR guidelines

- Keep PRs focused — one feature or fix per PR
- Include a clear description of what changed and why
- Reference any related issues
- Make sure CI passes before requesting review

## Questions?

Open an issue. We're friendly.
