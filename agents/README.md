# paw agents

12 specialized agents. Each owns a phase or review dimension.

## By phase

| Phase | Agents |
|---|---|
| Plan | architect, planner, devils-advocate |
| Build | builder |
| Review | code-reviewer, bug-auditor, security-reviewer, perf-checker, fe-reviewer, php-reviewer, test-runner |
| Document | docs-writer |

## By permission

| Tier | Agents | Can do |
|---|---|---|
| Read-only | architect, planner, devils-advocate, code-reviewer, bug-auditor, security-reviewer, perf-checker, fe-reviewer, php-reviewer | Look, report. Can't modify. |
| Read + Bash | test-runner | Run tests. Can't edit code. |
| Read + Write | docs-writer | Edit docs. Can't run commands. |
| Full | builder | Read, write, run. Use for implementation. |

## Standalone use

Every agent works individually:

```
> Use the security-reviewer agent to review this branch.
> Use the architect agent to design a solution for this spec.
> Use the fe-reviewer agent on the React components I just changed.
> Use the php-reviewer agent on the Laravel controllers in this PR.
```
