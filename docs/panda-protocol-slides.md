# Panda Protocol: Your AI Has No Standards
## Building an AI SDLC — and a starter kit you can clone today

---

### SLIDE 1 — Title

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          YOUR AI HAS NO STANDARDS                            ║
║                                                              ║
║          Building an AI SDLC That                            ║
║          Actually Enforces Yours                             ║
║                                                              ║
║          The Panda Protocol                                  ║
║          Episode: [##]                                       ║
║          Jay Fuller                                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

### SLIDE 2 — The Problem

```
  You:    "Add a login endpoint"

  AI:     ✓ Wrote the endpoint         ✗ No rate limiting
          ✓ Handles POST /login         ✗ No brute-force protection
          ✓ Returns a JWT               ✗ Logs password in plaintext
                                        ✗ JWT secret hardcoded
                                        ✗ No test
```

**Speaker notes:** The AI did exactly what you asked. The problem is what you didn't ask.

---

### SLIDE 3 — Two Choices

```
  OPTION A:  You review everything the AI writes.
             You are now a full-time AI babysitter.

  OPTION B:  You teach the AI your standards,
             and build a system that enforces them
             BEFORE the code reaches you.

  paw is Option B.
```

---

### SLIDE 4 — What Is An Agent?

```
  An agent is an LLM given a job.
  Same concept everywhere:

  MODEL     An LLM (Claude, GPT, etc.)
  CONTEXT   What it knows about the task
  PERSONA   How it behaves (reviewer, builder)
  SCOPE     What it's allowed to touch
  RULES     What standards it follows
  TOOLS     What actions it can take

  paw's agents are markdown files
  that define all six. No magic.
```

---

### SLIDE 5 — The Key Distinction

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
  └──────────┴──────────────┴──────────────┴──────────────┘

  Agents without skills are smart but uninformed.
  Skills without agents are knowledge with no one to use it.
  Hooks without either still enforce the rules.
```

---

### SLIDE 6 — paw Architecture

```
                    ┌──────────┐
                    │   YOU    │
                    └────┬─────┘
            ┌────────────┼────────────┐
            ▼            ▼            ▼
      ┌──────────┐ ┌──────────┐ ┌──────────┐
      │  AGENTS  │ │  SKILLS  │ │ CONTEXTS │
      │ 18 roles │ │  domain  │ │  mindset │
      └────┬─────┘ └──────────┘ └──────────┘
           │ reference     loaded by
           ▼                    │
      ┌──────────┐             │
      │  RULES   │◄────────────┘
      │ 6 pages  │
      └────┬─────┘
           │ enforced by
           ▼
      ┌──────────┐
      │  HOOKS   │  fire on Claude Code events
      └──────────┘
```

---

### SLIDE 7 — 18 Agents, Bounded Trust

```
  READ ONLY (10)    architect, planner, devils-advocate,
                    code-reviewer, bug-auditor, security,
                    perf-checker, fe-reviewer, php-reviewer,
                    rollback-planner
                    → They CANNOT modify your code.

  READ+BASH (3)     test-runner, integration-tester,
                    environment-checker
                    → Can run tests. CANNOT edit code.

  READ+WRITE (1)    docs-writer
                    → Can edit docs. CANNOT run commands.

  FULL (4)          builder, merge-resolver,
                    migration-architect, incident-commander
                    → Full power. Only 4 of 18.
```

---

### SLIDE 8 — Hooks: Hard Stops

```
  You type:  git rebase main

  ┌──────────────────────────────────────────────┐
  │  hooks/git_safety.py fires                   │
  │                                              │
  │  ✗ BLOCKED                                   │
  │                                              │
  │  "git rebase rewrites published history.     │
  │   Use 'git pull origin main' instead."       │
  │                                              │
  │  The command NEVER executes.                 │
  └──────────────────────────────────────────────┘
```

**Speaker notes:** Live demo. Type the command. Watch it get blocked.

---

### SLIDE 9 — The paw CLI

```
  paw setup             install hooks
  paw check             run 3 reviewers
  paw check --thorough  run all 8
  paw gate security     single agent
  paw suggest           detect your stack
  paw next              what to try next
  paw init              team config
  paw doctor            diagnose problems
  paw tutorial          learn paw (5 tracks)
  paw cheatsheet        quick reference
  paw desktop           Desktop launcher
```

---

### SLIDE 10 — Rules: Mechanical, Not Cultural

```
  BEFORE (tribal knowledge):
  "Hey, don't forget to write tests"
  "We don't rebase here"

  AFTER (mechanical enforcement):
  rules/test-first.md  → test-runner gate blocks
  rules/git-doctrine   → hooks/git_safety.py blocks

  Rule → Agent enforces → Hook prevents
```

---

### SLIDE 11 — Where This Goes: forge

```
  paw (today)                forge (when ready)
  ──────────                 ─────────────────

  18 agents                  46 agents
  Manual invocation          16-phase pipeline
  You sequence work          Orchestrator does
  You run reviews            15 gates parallel
  4 hooks                    8 + self-healing
  6 rules                    21 doctrine pages
```

**Speaker notes:** paw is the starter kit. forge is the full pipeline. You don't need forge to get value from paw.

---

### SLIDE 12 — Get Started Today

```
  git clone https://github.com/zofrus/paw.git ~/paw
  cd ~/paw
  ./paw setup
  ./paw tutorial

  Tech Forge hands-on session: [DATE]
```

---

### SLIDE 13 — Q&A

```
  paw:    github.com/zofrus/paw
  forge:  github.com/zofrus/forge  (preview)

  Questions?
```

---

## Presentation Flow (35 minutes)

| Time | Slides | What's happening |
|------|--------|-----------------|
| 0:00-3:00 | 1-2 | Hook: real AI mistake. No setup. |
| 3:00-5:00 | 3 | Two choices. Frame the problem. |
| 5:00-10:00 | 4-5 | What an agent is. The distinction table. |
| 10:00-14:00 | 6-7 | Architecture. Bounded trust. |
| 14:00-20:00 | 8 | **LIVE DEMO**: hooks block commands. |
| 20:00-25:00 | 9-10 | The CLI. Rules as enforcement. |
| 25:00-30:00 | 11 | Where this goes (forge preview). |
| 30:00-35:00 | 12-13 | Get started + Q&A. |
