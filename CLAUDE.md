# paw — AI SDLC starter kit

## What paw is

A lightweight, composable toolkit that gives your AI coding agent standards enforcement, specialized reviewers, and domain knowledge. Every piece works standalone.

## How to work in this repo

### Composability is the design
Every directory runs independently. Agents work without skills. Hooks work without agents. Rules are plain markdown anyone can read. Don't add cross-directory dependencies.

### Agents have scoped permissions
Most agents are read-only. Only the builder gets full access. This is intentional — trust through bounded autonomy.

### Rules are the source of truth
If a rule in `rules/` contradicts how an agent behaves, fix the agent. Rules don't bend to implementation convenience.

### Tests before code
The builder agent writes failing tests first, then implementation. The test-runner agent verifies. The auto_test_detect hook warns on missing tests.

## Git rules

- Always `git pull` (merge, not rebase) before push
- Never `git rebase` against published history
- Never `git push --force` to any branch
- Never commit to `main` directly — use a feature branch
- Always verify `git branch` shows the intended branch before committing

These are enforced by `hooks/git_safety.py` and `hooks/branch_guard.py`.

## Adding an agent

1. Pick the context it loads from `contexts/`.
2. Pick the rules it references from `rules/`.
3. Define minimum tools — least privilege.
4. Write the role, process, outputs, done-when.
5. Add to `agents/README.md`.

## Adding a rule

1. Write the statement, why, hard rules, soft rules.
2. Identify which agents/hooks enforce it.
3. Update relevant agents to reference the new rule.
4. Add to `rules/README.md`.
