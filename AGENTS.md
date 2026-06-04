# paw agents — for Codex CLI and other AI tools

This file tells AI coding tools about paw's agent definitions. If your tool reads `AGENTS.md` (like OpenAI Codex CLI), it will discover these agents automatically.

## How to use

Reference any agent by name in your prompt:

```
Use the security-reviewer agent to review this branch.
Use the architect agent to design a solution for [task].
Use the code-reviewer, bug-auditor, and security-reviewer on the current diff.
```

## Agent definitions

Each agent is a markdown file in `agents/` with frontmatter (name, description, model, tools) and a structured prompt body (role, context, rules, process, done-when).

| Agent | File | Purpose |
|---|---|---|
| architect | agents/architect.md | System architecture and design |
| planner | agents/planner.md | Implementation planning with workstreams |
| devils-advocate | agents/devils-advocate.md | Adversarial plan review |
| code-reviewer | agents/code-reviewer.md | General code review (correctness, edge cases) |
| bug-auditor | agents/bug-auditor.md | Latent bug hunting (race conditions, off-by-one) |
| security-reviewer | agents/security-reviewer.md | OWASP Top 10 security review |
| builder | agents/builder.md | TDD implementation (test first, then code) |
| test-runner | agents/test-runner.md | Run test suites, surface failures |
| perf-checker | agents/perf-checker.md | Performance review (N+1, unbounded fetches) |
| docs-writer | agents/docs-writer.md | Update docs to match code changes |
| fe-reviewer | agents/fe-reviewer.md | Frontend review (React/Vue, a11y, hooks) |
| php-reviewer | agents/php-reviewer.md | PHP/Laravel review (Eloquent, auth, queues) |
| merge-resolver | agents/merge-resolver.md | Intelligent merge conflict resolution |
| migration-architect | agents/migration-architect.md | Safe database migrations |
| incident-commander | agents/incident-commander.md | Production incident triage |
| rollback-planner | agents/rollback-planner.md | Rollback procedure planning |
| integration-tester | agents/integration-tester.md | Integration/E2E test execution |
| environment-checker | agents/environment-checker.md | Dev environment validation |

## Rules

Agents reference rules in `rules/`. Read them for the standards being enforced:

- `rules/git-doctrine.md` — Always merge, never rebase published history
- `rules/test-first.md` — Tests before code
- `rules/error-handling.md` — No silent failures
- `rules/no-secrets-in-code.md` — Secrets in env vars only
- `rules/branch-hygiene.md` — Feature branch per task
- `rules/security-basics.md` — Validate input, encode output

## Skills

Domain knowledge in `skills/`. Read for expertise:

- `skills/architecture/SKILL.md` — System decomposition, risk assessment
- `skills/security/SKILL.md` — OWASP Top 10, input validation, PII
- `skills/frontend/SKILL.md` — React, accessibility, performance
- `skills/php-laravel/SKILL.md` — Eloquent, middleware, migrations
- `skills/git-safety/SKILL.md` — Safe git operations
- `skills/quality-gate/SKILL.md` — Review checklist, severity rubric
- `skills/devils-advocate/SKILL.md` — Plan attack patterns
