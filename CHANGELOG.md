# Changelog

## 0.2.0 — 2026-06-04

### Added
- 6 new agents: merge-resolver, migration-architect, incident-commander, rollback-planner, integration-tester, environment-checker (18 total)
- Interactive TUI tutorial with sidebar navigation, bordered layout, ASCII art, typewriter and slide-in animations (17 pages, 7 sections)
- "The Key Distinction" page with color-coded comparison table (agents vs skills vs hooks)
- "What Is An Agent, Really?" page demystifying the term for non-technical audience
- Post-tutorial info screen with step-by-step next actions
- Setup script with requirement checks and automatic hook installation
- Cursor IDE integration (.cursor/rules/paw.mdc)
- Codex CLI integration (AGENTS.md)
- Per-line art colors in the TUI renderer

### Fixed
- git_safety.py: --force-with-lease no longer blocked (it's the safe alternative)
- git_safety.py: multi-line commands can no longer bypass regex patterns
- git_safety.py: `git checkout .` with chained commands now blocked
- branch_guard.py: fail-closed when git rev-parse fails (was fail-open)
- auto_test_detect.sh: JSON output properly escaped via python3 json.dumps
- Setup script: eliminated heredoc injection vulnerability
- Setup script: non-interactive mode no longer auto-installs without --yes flag
- All stale "12 agents" references updated to 18
- Permission tier counts corrected (10/3/1/4)
- Unicode column width handling in TUI renderer

## 0.1.0 — 2026-06-03

### Added
- 12 initial agents: architect, planner, devils-advocate, code-reviewer, bug-auditor, security-reviewer, builder, test-runner, perf-checker, docs-writer, fe-reviewer, php-reviewer
- 7 skills: architecture, devils-advocate, frontend, php-laravel, security, quality-gate, git-safety
- 4 hooks: git_safety.py, branch_guard.py, auto_test_detect.sh, _lib.py
- 6 rules: git-doctrine, test-first, error-handling, no-secrets-in-code, branch-hygiene, security-basics
- 4 contexts: dev, review, security, research
- CLAUDE.md project instructions
- README with quick start guide and architecture diagram
