# paw contexts

Four task-mode prompts. Set the agent's mindset based on what kind of work is happening.

| Context | When loaded | Mindset |
|---|---|---|
| [dev](dev.md) | Building, fixing, refactoring | Smallest change that works. Tests first. |
| [review](review.md) | Code review, quality gates | Assume nothing. Flag surprises. Be specific. |
| [security](security.md) | Security work, auth, PII | Adversarial. Trust nothing from outside. |
| [research](research.md) | Investigations, spikes | Read more than write. Produce written findings. |

Agents declare their default context. Multiple contexts can stack (e.g., security + review for a security audit).
