# Devil's Advocate Skill

**When to use:** Reviewing any plan before commitment — architecture, implementation plan, migration strategy, design proposal.

## Attack patterns

For every step in a plan, ask:

1. **What if it fails halfway?** — is there a recovery path, or are you stuck in a broken state?
2. **What if the input is wrong?** — garbage in, does it fail loudly or corrupt silently?
3. **What if this runs concurrently** with other work? Race conditions? Conflicting writes?
4. **What if this needs to work at 10x scale?** — does it still hold, or is there a hidden O(n^2)?
5. **What's the simplest version?** — is this overengineered for the actual requirement?

## Red flags to look for

- **"For now"** — means "forever" unless there's a ticket and a date
- **"We'll fix later"** — later never comes. If it matters, fix it now or accept the risk explicitly
- **Hand-waved steps** — "then we just deploy" / "the migration handles it" / "the API returns the data we need"
- **Missing error paths** — only the happy path is described
- **Implicit assumptions** — "users will have..." / "the data is always..."

## The 6-month test

Would a new team member, reading this plan in 6 months with no context, understand:
- What was decided and why?
- What was explicitly NOT done and why?
- What could go wrong and what the mitigation is?

If not, the plan is underspecified.

## Structuring concerns

- **Blockers** — must address before building. The plan doesn't work without this.
- **Warnings** — should address. Known risk if you don't.
- **Notes** — worth considering. Won't block but worth knowing.

Be specific. "This might have issues" is useless. "The batch job at step 3 has no timeout — if the API hangs, the job runs forever" is actionable.
