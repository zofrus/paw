# Contributing to paw

## Quick version

1. Fork the repo
2. Create a feature branch (`feat/your-change`)
3. Write tests for your change
4. Run `ruff check . && ruff format --check .` (must pass)
5. Run `python3 -m pytest tests/ -v` (must pass)
6. Submit a PR

## What to contribute

- **New agents** — follow the pattern in `agents/architect.md`. Pick a context, pick rules, define minimum tools.
- **New rules** — follow the pattern in `rules/git-doctrine.md`. Statement, why, hard rules, soft rules, enforced by.
- **New skills** — create `skills/your-skill/SKILL.md` with domain knowledge.
- **Bug fixes** — especially in hooks (security-critical code).
- **Tutorial improvements** — edit `tutorial_engine/content.py` for content, `tutorial_engine/engine.py` for rendering.

## Rules

- Tests before code. The `test-first` rule applies to paw itself.
- No secrets in code. No API keys, tokens, or credentials.
- Feature branch per change. Never commit to main directly.
- Hooks are security-critical. Changes to `hooks/` require tests.

## Style

- Python: ruff format + ruff check (no config needed, defaults are fine)
- Markdown: no linter, just be consistent with existing files
- Commits: imperative mood, short first line, explain the why

## Testing

```bash
python3 -m pytest tests/ -v
ruff check .
ruff format --check .
```

## Questions?

Open an issue. We're friendly.
