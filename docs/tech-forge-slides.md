# Tech Forge: Your AI Has No Standards (Let's Fix That)
## Hands-on — bring your laptop, clone the repo, build your AI SDLC

---

### SLIDE 1 — Title

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       YOUR AI HAS NO STANDARDS                               ║
║       (Let's Fix That)                                       ║
║                                                              ║
║       Tech Forge  ·  Jay Fuller                              ║
║       Hands-On Session                                       ║
║                                                              ║
║       Clone before we start:                                 ║
║       git clone https://github.com/zofrus/paw.git ~/paw     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

### SLIDE 2 — What We're Building Today

```
~/paw/
├── paw              CLI — the main entry point
├── agents/          18 specialized agents
├── skills/          7 domain knowledge bundles
├── hooks/           4 enforcement hooks
├── rules/           6 doctrine pages
├── contexts/        4 mindset modes
├── examples/        buggy app to practice on
└── tutorial         interactive walkthrough
```

"You should have this cloned. If not, do it now: `git clone https://github.com/zofrus/paw.git ~/paw`"

---

### SLIDE 3 — The Problem (Brief)

```
  You:    "Add a login endpoint"

  AI:     ✓ Wrote it          ✗ No rate limiting
          ✓ Returns JWT        ✗ Hardcoded secret
                               ✗ Logs the password
                               ✗ No test
```

"Today we stop talking about the problem and start fixing it."

---

### SLIDE 4 — HANDS-ON: Install paw

```
  cd ~/paw
  ./paw setup
```

"Everyone do this now. It checks Python, installs hooks, verifies everything works."

---

### SLIDE 5 — HANDS-ON: Watch Hooks Block

```
  Try in Claude Code:    git rebase main
                         → BLOCKED

  Try:                   git push --force
                         → BLOCKED

  Try:                   git commit -m "test"  (on main)
                         → BLOCKED

  Try:                   git push --force-with-lease
                         → ALLOWED (safe alternative)
```

---

### SLIDE 6 — HANDS-ON: Run a Review Agent

```
  Open a project with a diff. Type:

  > Use the code-reviewer agent on the current diff.

  Or use the CLI:

  paw check --quick

  Look at what it finds.
```

---

### SLIDE 7 — HANDS-ON: Stack Reviewers

```
  paw check

  Runs 3 agents:
    code-reviewer    → correctness, edge cases
    bug-auditor      → race conditions, off-by-one
    security-reviewer → OWASP Top 10, injection

  Three perspectives. Each catches different things.
```

---

### SLIDE 8 — Agent Permissions

```
  READ ONLY (10)   Can look. Can't touch.
  READ+BASH (3)    Can run tests. Can't edit.
  READ+WRITE (1)   Can edit docs. Can't run.
  FULL (4)         Full power. Only 4 of 18.

  The security-reviewer CANNOT modify your code.
  Trust through structural limitation.
```

---

### SLIDE 9 — DEMO: Plan, Critique, Build, Review

```
  > Use the architect agent to design [task]
  > Use the planner to turn it into a plan
  > Use the devils-advocate to critique
  > Use the builder to implement
  > Use the code-reviewer on the result
```

---

### SLIDE 10 — Smart Tools

```
  paw suggest      Detects your stack, recommends agents
  paw next         Shows what to try next
  paw doctor       Diagnoses problems
  paw cheatsheet   Quick reference (printable PDF too)
  paw init         Team config for your project
```

---

### SLIDE 11 — WORKSHOP: Write Your Own Rule (5 min)

```
  Pick one standard your team follows
  that ISN'T written down.

  Write it as a rule:

  # [Rule Name]
  **Statement:** One sentence.
  **Why:** Why this matters.
  ## Hard rules
  - ...
  **Enforced by:** which agent checks this?

  Drop it in the chat.
```

---

### SLIDE 12 — The Path Forward

```
  TODAY (paw)                  WHEN READY (forge)
  18 agents                    46 agents
  Manual invocation            16-phase pipeline
  paw check                    15 gates parallel
  4 hooks                      8 + self-healing

  paw is the starter kit.
  forge is the full pipeline.
```

---

### SLIDE 13 — What To Do Next

```
  TODAY:    Keep hooks on. Run paw check on a PR.
  THIS WEEK: Stack 3 reviewers on every PR.
  NEXT WEEK: Try the full workflow (5 agents).
  WHEN READY: Talk to Jay about forge.
```

---

### SLIDE 14 — Q&A

```
  paw repo:   github.com/zofrus/paw
  Full forge: github.com/zofrus/forge (preview)
  Cheatsheet: paw cheatsheet
  Questions?
```

---

## Timing (35 min + Q&A)

| Time | Slides | Activity |
|------|--------|----------|
| 0:00-3:00 | 1-3 | Intro + the problem |
| 3:00-8:00 | 4-5 | **HANDS-ON:** Install paw, watch hooks block |
| 8:00-15:00 | 6-7 | **HANDS-ON:** Run reviewers on your code |
| 15:00-18:00 | 8 | Agent permissions |
| 18:00-25:00 | 9-10 | **DEMO:** Full workflow + smart tools |
| 25:00-32:00 | 11 | **WORKSHOP:** Write a rule |
| 32:00-35:00 | 12-14 | Path forward + Q&A |
