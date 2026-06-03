# PHP / Laravel Skill

**When to use:** PHP or Laravel work — Eloquent, middleware, validation, queues, migrations, testing.

## Eloquent gotchas

- **N+1 queries** — use `with()` for eager loading. `$users->posts` in a loop = N+1. `User::with('posts')->get()` = 2 queries.
- **Mass assignment** — always use `$fillable` (allowlist), not `$guarded = []` (denylist of nothing)
- **Soft deletes** — `Model::all()` excludes soft-deleted by default. If you need them: `withTrashed()`. Know which you want.
- **Accessor performance** — never put a query inside an accessor/getter. It runs on every access.
- **Check-then-write** — use `firstOrCreate()` / `updateOrCreate()` instead of `if (!exists) create`. Avoids race conditions.

## Middleware patterns

- Apply auth middleware at the **route group** level, not per-route (easy to forget one)
- Rate limiting on auth endpoints: `throttle:5,1` minimum
- CORS configured at middleware level, not in individual controllers
- Order matters: auth before authorization before validation

## Form request validation

- Use **Form Request classes** for complex validation, not inline `$request->validate()`
- `authorize()` method for permission checks — returns `true`/`false`
- Custom error messages for user-facing forms
- `sometimes` rule for optional fields that should validate only when present

## Queue / job patterns

- **Idempotency** — jobs must be safe to retry. Use unique IDs or idempotency keys.
- **Set `$tries` and `$timeout`** on every job. Defaults are rarely correct.
- **Implement `failed()`** method for cleanup on permanent failure
- **Unique locks** — `ShouldBeUnique` interface when duplicate dispatch is harmful
- **Backoff** — use `$backoff` property for exponential retry delays

## Migration safety

- New columns: always `nullable()` or `->default()` — never break existing rows
- Never `dropColumn()` in production without a data backup plan
- Always write `down()` migration and test it
- Add indexes for columns used in WHERE clauses
- Separate migration deploy from code deploy when possible (expand/contract pattern)

## Testing

- **Feature tests** for HTTP endpoints (test the full request/response cycle)
- **Unit tests** for services and business logic (no framework, no database)
- **Database transactions** — use `RefreshDatabase` or `DatabaseTransactions` trait
- **Factories** for test data — never hardcode IDs or rely on seeders
- **Pest** preferred over PHPUnit for readability, but both work
