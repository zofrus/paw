# Building Your Own AI SDLC with paw

## What paw Is (30 seconds)

paw is **Personal Agent Workflows** — a composable AI SDLC starter kit. Instead of using AI as a fancy autocomplete, paw gives your AI agent specialized reviewers, enforced standards, and domain knowledge.

18 agents, each with a specific job and scoped permissions. 7 skill bundles. 4 hooks that mechanically block dangerous operations. 6 rules that are enforced, not suggested. A CLI that ties it all together.

paw is extracted from forge, a full 16-phase multi-agent delivery pipeline. paw is the pieces you can adopt today — no pipeline required.

## Why Build Your Own AI SDLC

**The core problem:** Off-the-shelf AI coding tools (Copilot, Cursor, etc.) optimize for *generation speed*. They don't optimize for *correctness, reviewability, or organizational trust*. That gap is where bugs, security holes, and "works on my machine" live.

**Three reasons to build your own:**

### 1. You encode YOUR team's standards, not generic ones

Every team has opinions: how migrations work, what "reviewed" means, which security checks matter. paw's `rules/` directory has 6 doctrine pages — things like "tests before code, always" and "no silent failures, ever." These aren't suggestions; they're enforced by hooks and gates. Your team's hard-won lessons become **mechanical enforcement**, not tribal knowledge that new hires forget.

### 2. Trust through bounded autonomy

The biggest blocker to AI adoption isn't capability — it's trust. paw solves this by giving each agent **least-privilege access**. The architect agent is read-only. The security reviewer can't modify code. Only 4 of 18 agents get full access. A devil's advocate agent explicitly tries to poke holes in the plan *before* any code is written.

This means you can delegate a larger chunk of work and trust that the system catches mistakes — not because the AI is perfect, but because **the system is designed to catch imperfection**.

### 3. Composability means you adopt at your own pace

You don't have to go all-in. Want just the git safety hooks? Run `paw setup`. Want a quality check on your existing PR? Run `paw check`. Want the full plan-build-review workflow? Use the agents step by step. Every piece works independently.

## The Architecture

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
      └──────────┘
```

- **Agents** (18) — the workers, each with scoped permissions
- **Skills** (7) — domain knowledge bundles
- **Rules** (6) — doctrine, the source of truth
- **Hooks** (4) — mechanical enforcement
- **Contexts** (4) — mindset modes (dev, review, security, research)

## First Steps to Get Started

### Day 1: Clone and run setup

```bash
git clone https://github.com/zofrus/paw.git ~/paw
cd ~/paw
./paw setup
```

This installs git guardrails (blocks rebase, force-push, commits to main) and verifies your environment. Takes 2 minutes.

### Day 1: Run the tutorial

```bash
paw tutorial
```

5 tracks covering concepts, hands-on setup, the CLI, advanced workflows, and practice against a buggy app.

### Week 1: Run review agents on real PRs

```bash
paw check          # code-reviewer + bug-auditor + security-reviewer
paw gate security  # just the OWASP Top 10 review
```

See what they catch that your current review process doesn't.

### Week 2: Try the full workflow

```
> Use the architect agent to design a solution for [task].
> Use the planner agent to turn it into a plan.
> Use the devils-advocate agent to critique it.
> Use the builder agent to implement.
> Use the code-reviewer agent on the result.
```

### Then: Customize for your team

Add rules for your domain. Disable agents you don't need (`paw init`). Write new agents for your stack. The point of building your own is that **you own it**.

## Where This Goes: forge

paw is the starter kit. forge is the full pipeline:

| paw | forge |
|---|---|
| 18 agents | 46 agents |
| Manual invocation | 16-phase automated pipeline |
| You sequence work | Orchestrator sequences it |
| You run reviews | 15 gates run in parallel |
| 4 hooks | 8 + self-healing + heartbeat |
| 6 rules | 21 doctrine pages |

Start with paw. Graduate to forge when you're ready.

## TL;DR

AI coding tools give you speed. An AI SDLC gives you speed *with guardrails your team controls*. paw is how you start — composable pieces you adopt incrementally.

Questions? Hit up @jfuller.
