---
description: Root-cause a single failing test - reproduce, inspect, isolate, and propose the minimal fix.
---

## User Input

```text
$ARGUMENTS  (the failing test name or REQ-NNN)
```

## Outline

Deep single-failure investigation, adapted from gstack's investigate flow. Use
when `speckit.qa.run` could not auto-classify a failure, or for a flaky test.

1. Identify the target test from `$ARGUMENTS` (a test name or `REQ-NNN`) and the
   feature directory via `.specify/feature.json`.

2. **Reproduce deterministically.** Run just that test 3x. Record whether it
   fails always (deterministic) or intermittently (flaky per the constitution's
   flaky definition).

3. **Gather signal** for the failing layer:
   - UI/web → browser console + network log + DOM at the failing step
     (screenshot as evidence), via the configured driver.
   - API → the exact request, response status/body, and which assertion broke.

4. **Form one hypothesis, then test it** - change a single variable
   (selector, wait, payload, env) and re-run. Iterate until the cause is
   isolated. Do not shotgun multiple changes at once.

5. **Classify and fix** as in `speckit.qa.run` (selector drift / timing / real
   app bug / bad expectation). Keep the fix minimal and in the correct file
   (locator file, test, or a spec `clarify` flag). For flakiness, prefer a
   proper wait or a deterministic fixture over a retry.

6. **Report** the root cause in one paragraph, the single fix applied (or the
   finding to escalate), and whether the test is now deterministic.
