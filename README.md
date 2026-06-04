# paw — Personal Agent Workflows

```
        _______________
       /               \
      |  ┌───┐ ┌───┐  |
      |  │ ● │ │ ● │  |
      |  └───┘ └───┘  |
      |      ___      |
      |     /   \     |
      |    | ◡◡◡ |    |
       \   \_____/   /
        \___________/
         /    |    \
        🐾   🐾   🐾

     p a w
     Personal Agent Workflows
     an AI SDLC starter kit
```

> Your AI agent writes code fast. paw makes sure it writes code *right*.

## What is this?

paw is a lightweight, composable AI SDLC (Software Development Lifecycle) toolkit. It gives your AI coding agent:

- **Standards that are enforced, not suggested** — rules that hooks block on, not READMEs people skip
- **Specialized reviewers** — 18 agents that each check a different dimension of code quality
- **Domain knowledge** — 7 skill bundles for architecture, security, frontend, PHP/Laravel, and more
- **Git guardrails** — hooks that mechanically prevent rebase, force-push, and commits to main

paw is extracted from [forge](https://github.com/zofrus/forge), a full 16-phase multi-agent delivery pipeline. paw is the starter kit — the pieces you can adopt today without the full pipeline.

## What's inside

```
paw/
├── agents/          18 specialized agents
│   ├── architect.md         planner.md
│   ├── devils-advocate.md   rollback-planner.md
│   ├── code-reviewer.md     bug-auditor.md
│   ├── security-reviewer.md perf-checker.md
│   ├── fe-reviewer.md       php-reviewer.md
│   ├── builder.md           merge-resolver.md
│   ├── migration-architect.md
│   ├── incident-commander.md
│   ├── test-runner.md       integration-tester.md
│   ├── environment-checker.md
│   └── docs-writer.md
│
├── skills/          7 domain knowledge bundles
│   ├── architecture/
│   ├── devils-advocate/
│   ├── frontend/
│   ├── php-laravel/
│   ├── security/
│   ├── quality-gate/
│   └── git-safety/
│
├── hooks/           4 enforcement hooks
│   ├── git_safety.py
│   ├── branch_guard.py
│   ├── auto_test_detect.sh
│   └── _lib.py
│
├── rules/           6 doctrine pages
│   ├── git-doctrine.md
│   ├── test-first.md
│   ├── error-handling.md
│   ├── no-secrets-in-code.md
│   ├── branch-hygiene.md
│   └── security-basics.md
│
├── contexts/        4 task-mode prompts
│   ├── dev.md
│   ├── review.md
│   ├── security.md
│   └── research.md
│
├── setup            checks requirements, installs hooks
├── tutorial         interactive TUI walkthrough
├── tutorial_engine/ tutorial rendering engine
│
├── CLAUDE.md        project instructions (Claude Code)
├── AGENTS.md        agent index (Codex CLI)
└── .cursor/rules/   Cursor IDE integration
```

## Getting started

### 1. Clone and run setup

```bash
# Clone anywhere you want — paw detects its own location at runtime
git clone https://github.com/zofrus/paw.git ~/paw
cd ~/paw
./setup
```

Clone to any path — `~/paw`, `~/tools/paw`, your projects directory, wherever. The setup script detects its own location and writes the correct absolute paths to your Claude Code settings. No hardcoded paths.

Setup checks everything you need (Python 3.10+, curses, git, terminal size, Claude Code) and walks you through installing hooks. If anything's missing, it tells you exactly how to fix it for your platform. It backs up your Claude Code settings before touching them.

### 2. Run the interactive tutorial

```bash
./tutorial
```

```
  ┌──────────────────────────────────────────────────────┐
  │                                                      │
  │   17 pages  ·  7 sections  ·  ~5 minutes             │
  │                                                      │
  │   [</>] Navigate   [s] Skip section   [q] Quit       │
  │                                                      │
  │   Covers: what paw is, agents, hooks, rules,         │
  │   how to install, how to customize.                   │
  │                                                      │
  │   Requires: Python 3.10+, 80x24+ terminal            │
  │   Dependencies: none (Python stdlib only)             │
  │                                                      │
  └──────────────────────────────────────────────────────┘
```

Animations are interruptible — any keypress during a typewriter or slide-in effect completes it instantly. You're never trapped waiting.

## Quick start

### Option 1: Run setup (recommended)

```bash
git clone https://github.com/zofrus/paw.git ~/paw
cd ~/paw
./setup
```

Setup checks requirements, installs hooks (using the actual clone path, not a hardcoded one), and verifies everything works. If you want to install hooks manually instead, see `hooks/README.md`.

### Option 2: Agents on demand (10 minutes)

Use any agent by name in Claude Code:

```
> Use the security-reviewer agent to review this branch.
> Use the architect agent to design a solution for adding password reset.
> Use the fe-reviewer agent on the React components I just changed.
> Use the bug-auditor agent on the current diff.
> Use the php-reviewer agent on the Laravel controllers in this PR.
```

### Option 3: Full quality review

Run multiple review agents for a comprehensive check:

```
> Use the code-reviewer agent, then the bug-auditor agent,
  then the security-reviewer agent on the current diff.
```

Three independent perspectives — correctness, latent bugs, and security — each from a specialist.

### Option 4: Plan, Build, Review workflow

The full lightweight SDLC:

```
> Use the architect agent to design a solution for [your task].
> Use the planner agent to turn the architecture into a plan.
> Use the devils-advocate agent to critique the plan.
> Use the builder agent to implement workstream 1.
> Use the code-reviewer agent on the changes.
```

## How it works

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  AGENTS  │────▶│  SKILLS  │     │ CONTEXTS │
│ 18 roles │     │  domain  │     │  mindset │
│ scoped   │     │  know-   │     │  modes   │
│ perms    │     │  ledge   │     │          │
└────┬─────┘     └──────────┘     └──────────┘
     │                                  │
     │ reference                   loaded by
     ▼                                  │
┌──────────┐                            │
│  RULES   │◄───────────────────────────┘
│ 6 pages  │
└────┬─────┘
     │ enforced by
     ▼
┌──────────┐
│  HOOKS   │  ◄── fire on Claude Code events
│ 4 files  │
└──────────┘
```

- **Agents** do the work. Each has scoped permissions (most are read-only).
- **Skills** provide domain knowledge. Agents load them for expertise.
- **Contexts** set the mindset (building vs reviewing vs security audit).
- **Rules** are the source of truth. Agents reference them.
- **Hooks** enforce rules mechanically. They fire on Claude Code events.

## Agent permissions

Most agents can only read. This is by design.

| Tier | Agents | Can do |
|---|---|---|
| **Read-only** | architect, planner, devils-advocate, code-reviewer, bug-auditor, security-reviewer, perf-checker, fe-reviewer, php-reviewer, rollback-planner | Look and report. Cannot modify. |
| **Read + Bash** | test-runner, integration-tester, environment-checker | Run tests/checks. Cannot edit code. |
| **Read + Write** | docs-writer | Edit docs. Cannot run commands. |
| **Full** | builder, merge-resolver, migration-architect, incident-commander | Implementation and operations. |

## Customizing

### Add a rule

Create `rules/your-rule.md`:

```markdown
# Your Rule Name

**Statement:** One sentence.

**Why:** Why this matters.

## Hard rules
- ...

## Soft rules
- ...

**Enforced by:** which agents/hooks check this.
```

Then reference it in the relevant agent's Rules section.

### Add an agent

Create `agents/your-agent.md` with frontmatter:

```yaml
---
name: your-agent
description: What it does in one line.
model: sonnet
tools: Read, Grep, Glob
---
```

Then add: Role, Context, Rules, Process, Done when.

### Add a skill

Create `skills/your-skill/SKILL.md` with the domain knowledge. Reference it from relevant agents.

## Works with

### Claude Code

paw was built for Claude Code. Agents, hooks, skills, and contexts integrate natively. Run `./setup` to install hooks, then invoke agents by name.

### Cursor

paw ships with `.cursor/rules/paw.mdc` — Cursor loads it automatically. It references all agents, skills, and rules so Cursor knows your team's standards. No configuration needed beyond cloning the repo into your project.

### OpenAI Codex CLI

paw ships with `AGENTS.md` at the repo root. Codex CLI reads this file to discover agent definitions. Reference agents by name in your prompts just like Claude Code.

### Any AI coding tool

The agents, rules, and skills are plain markdown files. Any tool that reads markdown context (Windsurf, Aider, Continue, etc.) can use them. Point your tool at the relevant `.md` file.

## What this is NOT

- **Not a pipeline.** paw is tools, not a workflow. You invoke what you need.
- **Not a replacement for human review.** Agents augment. Humans decide.
- **Not opinionated about your stack.** Works with any language, any framework.
- **Not a vendor product.** You own it. Fork it. Change it. Delete what you don't need.

## Want the full pipeline?

paw is the starter kit. [forge](https://github.com/zofrus/forge) is the full 16-phase delivery pipeline with 46 agents, 15 parallel quality gates, self-healing, heartbeat monitoring, and durable state. Start with paw, graduate to forge when you're ready.

## License

MIT
