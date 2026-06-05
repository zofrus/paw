# paw Architecture — How It All Fits Together

## The Full Picture

```
                    ┌──────────┐
                    │   YOU    │  paw setup / paw check / prompt
                    └────┬─────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
   ┌──────────┐    ┌──────────┐    ┌──────────┐
   │  AGENTS  │    │  SKILLS  │    │ CONTEXTS │
   │ 18 roles │    │  domain  │    │  mindset │
   │  scoped  │    │  know-   │    │  modes   │
   │  perms   │    │  ledge   │    │          │
   └────┬─────┘    └──────────┘    └──────────┘
        │                ▲               ▲
        │ reference      │  loaded by    │
        ▼                │               │
   ┌──────────┐          │               │
   │  RULES   │──────────┘───────────────┘
   │ 6 pages  │
   └────┬─────┘
        │ enforced by
        ▼
   ┌──────────┐
   │  HOOKS   │  fire on Claude Code / git events
   │ 4 files  │
   └──────────┘
```

## The Key Distinction

```
┌──────────┬──────────────┬──────────────┬──────────────┐
│          │   AGENTS     │   SKILLS     │   HOOKS      │
├──────────┼──────────────┼──────────────┼──────────────┤
│ What     │ AI actors    │ Knowledge    │ Scripts      │
│ Has AI?  │ Yes          │ No (teaches) │ No (enforces)│
│ Decides? │ Yes-judgment │ No-informs   │ No-reacts    │
│ Runs     │ On dispatch  │ When loaded  │ On events    │
│ Can fail │ Yes (retry)  │ N/A          │ Yes (blocks) │
│ Count    │ 18           │ 7            │ 4            │
│ Lives in │ agents/      │ skills/      │ hooks/       │
└──────────┴──────────────┴──────────────┴──────────────┘

Agents without skills are smart but uninformed.
Skills without agents are knowledge with no one to use it.
Hooks without either still enforce the rules — that's the point.
```

## Agent Permissions — Bounded Trust

```
┌─────────────────────────────────────────────────────────────┐
│              AGENT PERMISSION TIERS                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  READ ONLY (10 agents)                                      │
│  architect, planner, devils-advocate, rollback-planner,     │
│  code-reviewer, bug-auditor, security-reviewer,             │
│  perf-checker, fe-reviewer, php-reviewer                    │
│  → They CANNOT modify your code.                            │
│                                                             │
│  READ + BASH (3 agents)                                     │
│  test-runner, integration-tester, environment-checker       │
│  → Can run tests. CANNOT edit source files.                 │
│                                                             │
│  READ + WRITE (1 agent)                                     │
│  docs-writer                                                │
│  → Can update docs. CANNOT run commands.                    │
│                                                             │
│  FULL ACCESS (4 agents)                                     │
│  builder, merge-resolver, migration-architect,              │
│  incident-commander                                         │
│  → Full power, but only 4 of 18.                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## The paw CLI

```
┌─────────────────────────────────────────────────────────────┐
│  SETUP                                                      │
│    paw setup          install hooks + check requirements    │
│    paw doctor         diagnose problems                     │
│    paw desktop        Desktop launcher (macOS)              │
│    paw init           team config (.paw.json)               │
│    paw suggest        detect stack + recommend agents       │
│    paw next           what to try next                      │
│                                                             │
│  QUALITY GATES                                              │
│    paw check --quick    code-reviewer only                  │
│    paw check            code + bugs + security              │
│    paw check --thorough all 8 reviewers                     │
│    paw gate <name>      single agent                        │
│                                                             │
│  LEARN                                                      │
│    paw tutorial         TUI (5 tracks)                      │
│    paw tutorial --web   browser version                     │
│    paw cheatsheet       quick reference                     │
│    paw agents           list all 18                         │
└─────────────────────────────────────────────────────────────┘
```

## Use What You Want

```
WANT ONLY THIS?                     DO THIS:
─────────────────────────────────────────────────────────

Git guardrails                       paw setup
Quality check on any PR              paw check
Single gate (e.g. security)          paw gate security
Smart stack detection                paw suggest
Full plan-build-review workflow      5 agent prompts
Printable reference                  paw cheatsheet
Desktop app for non-technical users  paw desktop
The full 46-agent pipeline           forge (when ready)
```

## Where paw Goes: forge

```
paw (starter kit)              forge (full pipeline)
─────────────────              ─────────────────────

18 agents                      46 agents
Manual invocation              16-phase automated pipeline
You sequence the work          Orchestrator sequences it
You run reviews                15 gates run in parallel
4 hooks                        8 hooks + self-healing
6 rules                        21 doctrine pages
paw check                      /forge "your spec here"

Start with paw. Graduate to forge when you're ready.
```
