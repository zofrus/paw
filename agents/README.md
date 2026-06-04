# paw agents

18 specialized agents. Each owns a phase or review dimension.

## By phase

| Phase | Agents |
|---|---|
| Plan | architect, planner, devils-advocate, rollback-planner |
| Build | builder, merge-resolver, migration-architect |
| Review | code-reviewer, bug-auditor, security-reviewer, perf-checker, fe-reviewer, php-reviewer, test-runner, integration-tester, environment-checker |
| Respond | incident-commander |
| Document | docs-writer |

## By permission

| Tier | Agents | Can do |
|---|---|---|
| Read-only | architect, planner, devils-advocate, code-reviewer, bug-auditor, security-reviewer, perf-checker, fe-reviewer, php-reviewer, rollback-planner | Look, report. Can't modify. |
| Read + Bash | test-runner, integration-tester, environment-checker | Run tests/checks. Can't edit code. |
| Read + Write | docs-writer | Edit docs. Can't run commands. |
| Full | builder, merge-resolver, migration-architect, incident-commander | Read, write, run. Use for implementation and operations. |

## Standalone use

Every agent works individually:

```
> Use the security-reviewer agent to review this branch.
> Use the architect agent to design a solution for this spec.
> Use the merge-resolver agent to resolve the current conflicts.
> Use the migration-architect agent to plan the schema change.
> Use the rollback-planner agent on the current diff.
> Use the incident-commander agent to triage this production issue.
> Use the environment-checker agent to validate my dev setup.
```

## Works with

- **Claude Code** — invoke agents by name in the CLI or IDE extensions
- **Cursor** — add agent .md files as custom rules or @docs references
- **Codex CLI** — reference agents in your Codex instructions or AGENTS.md
