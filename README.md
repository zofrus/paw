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

paw is a composable AI SDLC toolkit. It gives your AI coding agent:

- **Standards that are enforced, not suggested** — hooks that block, not READMEs people skip
- **Specialized reviewers** — 18 agents that each check a different dimension
- **Domain knowledge** — 7 skill bundles for architecture, security, frontend, PHP, and more
- **Git guardrails** — mechanically prevent rebase, force-push, and commits to main
- **A CLI** — `paw check`, `paw gate security`, `paw doctor`, `paw init`

paw is extracted from [forge](https://github.com/zofrus/forge), a full 16-phase multi-agent delivery pipeline. paw is the starter kit.

## Getting started

```bash
git clone https://github.com/zofrus/paw.git ~/paw
cd ~/paw
./paw setup
```

Clone anywhere — `~/paw`, `~/tools/paw`, wherever. Setup detects its own location and writes correct paths. It checks Python 3.10+, curses, git, terminal, and Claude Code. Backs up your settings before touching them.

## The paw CLI

```
paw setup              Check requirements, install hooks
paw tutorial            Interactive TUI walkthrough (5 tracks)
paw tutorial --web      Open the browser-based tutorial
paw doctor              Diagnose problems with your install
paw init                Scaffold .paw.json config into a project
paw check               Standard quality gate (3 reviewers)
paw check --quick       Quick gate (code-reviewer only)
paw check --thorough    Thorough gate (all 8 reviewers)
paw gate <name>         Run a single review agent
paw agents              List all 18 agents
paw next                Suggested next steps based on progress
paw suggest             Detect your stack, recommend agents
paw cheatsheet          Print the quick reference card
paw desktop             Create a Desktop app launcher (macOS)
paw uninstall           Remove hooks and symlink
paw completions         Shell tab-completion (zsh | bash)
paw version             Show version
```

## Tutorials

Two ways to learn paw:

### Terminal (TUI)

```bash
./paw tutorial
```

Interactive walkthrough with sidebar navigation, ASCII art, and typewriter animations. 17 pages, 7 sections, ~5 minutes. Choose between:

- **Learn paw** — what paw is, how it works, the components
- **Hands-on** — install hooks, run agents, write a rule

### Browser

```bash
open tutorial.html         # macOS — opens directly, no server needed
# or: ./paw tutorial --web
```

Self-contained HTML file — no server required. Dark theme, sidebar navigation, keyboard shortcuts (arrow keys, Escape). 7 tracks including hands-on workshops and contributor guide.

## What's inside

```
paw/
├── paw              CLI — the main entry point
├── setup            requirement checker + hook installer
├── tutorial         TUI walkthrough (curses)
├── tutorial.html    browser walkthrough
│
├── agents/          18 specialized agents
│   ├── architect        planner          devils-advocate
│   ├── rollback-planner builder          merge-resolver
│   ├── migration-architect               incident-commander
│   ├── code-reviewer    bug-auditor      security-reviewer
│   ├── perf-checker     fe-reviewer      php-reviewer
│   ├── test-runner      integration-tester
│   ├── environment-checker               docs-writer
│   └── README.md
│
├── skills/          7 domain knowledge bundles
│   ├── architecture/    devils-advocate/  frontend/
│   ├── php-laravel/     security/         quality-gate/
│   └── git-safety/
│
├── hooks/           enforcement hooks
│   ├── git_safety.py        block rebase, force-push, reset --hard
│   ├── branch_guard.py      block commits on main/master/develop
│   ├── auto_test_detect.sh  warn on missing test files
│   ├── install_hooks.py     settings.json installer
│   └── _lib.py              shared helpers
│
├── rules/           6 doctrine pages
│   ├── git-doctrine     test-first       error-handling
│   ├── no-secrets       branch-hygiene   security-basics
│   └── README.md
│
├── contexts/        4 mindset modes
│   ├── dev    review    security    research
│   └── README.md
│
├── examples/        practice targets
│   └── buggy-app/   intentionally buggy app for training
│
├── tests/           64 tests (hooks, navigation, content)
├── CLAUDE.md        Claude Code integration
├── AGENTS.md        Codex CLI integration
├── .cursor/rules/   Cursor IDE integration
├── .pre-commit-hooks.yaml  git pre-commit framework
├── pyproject.toml   Python project config
├── CONTRIBUTING.md  how to contribute
├── CHANGELOG.md     version history
└── LICENSE          MIT
```

## How it works

```
                    ┌──────────┐
                    │   YOU    │  type a command or prompt
                    └────┬─────┘
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
      ┌──────────┐ ┌──────────┐ ┌──────────┐
      │  AGENTS  │ │  SKILLS  │ │ CONTEXTS │
      │ 18 roles │ │  domain  │ │  mindset │
      │  scoped  │ │  know-   │ │  modes   │
      │  perms   │ │  ledge   │ │          │
      └────┬─────┘ └──────────┘ └──────────┘
           │              ▲            ▲
           │ reference    │  loaded by │
           ▼              │            │
      ┌──────────┐        │            │
      │  RULES   │────────┘────────────┘
      │ 6 pages  │
      └────┬─────┘
           │ enforced by
           ▼
      ┌──────────┐
      │  HOOKS   │  fire on Claude Code / git events
      │ 4 files  │
      └──────────┘
```

- **Agents** do the work. 18 roles, most read-only. Scoped permissions.
- **Skills** provide domain knowledge. Agents load them for expertise.
- **Contexts** set the mindset — building vs reviewing vs security audit.
- **Rules** are the source of truth. Agents reference them.
- **Hooks** enforce rules mechanically. Hard stops, not suggestions.

## Quality gates

Three presets for different situations:

| Preset | Agents | When to use |
|---|---|---|
| `paw check --quick` | code-reviewer | Fast feedback during development |
| `paw check` | code-reviewer, bug-auditor, security-reviewer | Before requesting code review (default) |
| `paw check --thorough` | 8 reviewers (code, bugs, security, perf, tests, docs, + stack-specific) | Before merging significant features |

Or run a single gate: `paw gate security`, `paw gate bugs`, `paw gate perf`

## Agent permissions

14 of 18 agents have restricted permissions. Trust through structural limitation.

| Tier | Agents | Can do |
|---|---|---|
| **Read-only** (10) | architect, planner, devils-advocate, rollback-planner, code-reviewer, bug-auditor, security-reviewer, perf-checker, fe-reviewer, php-reviewer | Look and report. Cannot modify. |
| **Read + Bash** (3) | test-runner, integration-tester, environment-checker | Run tests/checks. Cannot edit code. |
| **Read + Write** (1) | docs-writer | Edit docs. Cannot run commands. |
| **Full** (4) | builder, merge-resolver, migration-architect, incident-commander | Implementation and operations. |

## Team config

Scaffold a `.paw.json` into your project to customize for your team:

```bash
paw init
```

This creates `.paw.json` with:
- **agents.enabled** — which agents run for this project
- **agents.disabled** — which to skip (e.g., disable `php-reviewer` for a JS project)
- **quality_gate.default_preset** — your team's default check level
- **history** — opt-in run logging to `.paw/history.jsonl`

Check `.paw.json` into version control so your team shares the config.

`paw suggest` auto-detects your stack (Node.js, PHP/Laravel, Python, Go, Rust) and recommends which agents to enable.

## Smart suggestions

```bash
paw next                # What should I do next?
paw suggest             # Which agents fit my project?
paw cheatsheet          # Quick reference card (terminal)
```

`paw next` tracks your progress and suggests the next step you haven't tried. `paw suggest` reads your project files and recommends agents. `paw cheatsheet` prints a one-screen reference card with all commands, agents, prompts, and workflows.

The cheatsheet is also available as a [printable PDF](cheatsheet.html) — open in a browser and hit Cmd+P.

## Works with

| Tool | Integration | Setup |
|---|---|---|
| **Claude Code** | Native — hooks, agents, skills, contexts | `paw setup` |
| **Cursor** | `.cursor/rules/paw.mdc` auto-loaded | Clone paw into your project |
| **Codex CLI** | `AGENTS.md` discovered automatically | Clone paw into your project |
| **pre-commit** | `.pre-commit-hooks.yaml` | Add paw repo to `.pre-commit-config.yaml` |
| **Any tool** | Plain markdown files | Point your tool at the `.md` file |

## Customizing

### Add a rule

```markdown
# Your Rule Name
**Statement:** One sentence.
**Why:** Why this matters.
## Hard rules
- ...
**Enforced by:** which agents/hooks check this.
```

### Add an agent

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

Create `skills/your-skill/SKILL.md` with domain knowledge. Reference it from agents.

## Practice

Run agents against the example buggy app:

```bash
paw gate security    # then point it at examples/buggy-app/
```

The app has 6 security holes, 4 latent bugs, an N+1 query, and zero tests. See `examples/buggy-app/README.md` for the full list (spoiler-tagged).

## Troubleshooting

```bash
paw doctor
```

Checks: Python version, curses module, hook files, settings.json, agent count, hook self-test, and test suite. Tells you exactly what's wrong and how to fix it.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

**Before submitting a PR**, run these checks locally:

```bash
python3 -m pytest tests/ -v      # 64 tests must pass
ruff check .                     # zero lint errors
ruff format --check .            # formatting must match
```

All PRs require maintainer approval before merging. Open an issue first for large changes so we can discuss the approach.

## Want the full pipeline?

paw is the starter kit. [forge](https://github.com/zofrus/forge) is the full 16-phase delivery pipeline with 46 agents, 15 parallel quality gates, self-healing, heartbeat monitoring, and durable state. Start with paw, graduate to forge when you're ready.

## License

MIT
