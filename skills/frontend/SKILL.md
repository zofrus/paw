# Frontend Skill

**When to use:** React, Vue, or Angular work — component design, accessibility, performance, state management.

## Component design

- **Composition over inheritance** — build complex UI from small, focused components
- **Single responsibility** — one component, one job. If the name needs "And", split it.
- **Props interface** — keep it narrow. More than 5-7 props? The component is doing too much.
- **Prop drilling limit** — more than 2 levels deep? Use context or composition (children pattern).
- **Children pattern** — prefer `<Layout><Content /></Layout>` over render props when possible.

## Hooks best practices (React)

- **Dependency arrays must be complete** — ESLint rule `react-hooks/exhaustive-deps` is not optional
- **Effects clean up** — return a cleanup function for subscriptions, timers, event listeners
- **Custom hooks** — extract reusable stateful logic into `useXxx` hooks
- **Never call hooks conditionally** — hooks must be called in the same order every render
- **Avoid `useEffect` for derived state** — compute it during render instead

## Accessibility floor (WCAG 2.1 AA)

These are minimums, not aspirations:

- Every interactive element has an accessible label (`aria-label`, associated `<label>`, or visible text)
- Color contrast: 4.5:1 for normal text, 3:1 for large text
- All functionality reachable via keyboard (Tab, Enter, Escape, Arrow keys)
- Focus management: focus moves logically on route change and modal open/close
- ARIA landmarks on major sections (`<main>`, `<nav>`, `<aside>`)
- Images: meaningful `alt` text, or `alt=""` for decorative
- Form errors announced to screen readers (`aria-live` or `role="alert"`)

## Performance

- **Memoization** — `React.memo`, `useMemo`, `useCallback` only where there's measured need. Don't prematurely optimize.
- **Virtualization** — lists >100 items should use `react-window` or similar
- **Code splitting** — at minimum, split at the route level (`React.lazy` + `Suspense`)
- **Image optimization** — responsive sizes, lazy loading below the fold, modern formats (WebP/AVIF)
- **Bundle awareness** — check import cost. A 500KB library for one function is not worth it.

## State management

- **Local state first** — `useState` until two components need the same state
- **Lift when needed** — move state to the nearest common ancestor
- **Global for cross-cutting only** — auth, theme, locale. Not form state.
- **Derived state is computed, not stored** — don't duplicate state that can be calculated
- **Key props** — must be stable and unique. Never use array index as key on dynamic lists.
