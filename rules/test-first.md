# Test First

**Statement:** Tests written before or alongside code. Never after.

**Why:** Tests written after anchor on the implementation, not the requirement. They confirm what the code does, not what it should do. Test-first forces you to make the spec concrete before the implementation locks it in.

## Hard rules

- For every new function/module/route, a test file exists in the same PR
- New code with zero tests cannot pass the review gate
- Bug fixes ship with a regression test that fails on the buggy code and passes on the fix
- Tests must actually exercise behavior — not just import the module

## Soft rules

- Prefer one assertion per test where reasonable
- Test the contract, not the implementation — don't assert on private internals
- Cover unhappy paths explicitly (errors, edge cases, boundaries)
- Integration tests for cross-process/network/disk; unit tests for pure logic

## How to apply

| Situation | Wrong | Right |
|---|---|---|
| New feature | Write code, then write tests that pass | Write failing test, then write code to pass it |
| Bug fix | Fix the bug, ship | Write test that reproduces bug, verify it fails, fix, verify it passes |
| Refactor | Refactor, hope nothing broke | Verify existing tests pass, refactor, verify tests still pass |

**Enforced by:** `agents/test-runner`, `hooks/auto_test_detect.sh`
