---
description: Run the generated suite for a feature; QA any UI failures with browser-captured evidence and propose fixes.
---

## User Input

```text
$ARGUMENTS
```

## Outline

Run-and-QA loop, adapted from gstack's QA flow. Executes the generated suite,
then for UI/web failures uses the browser to gather evidence and propose a
targeted fix - without rewriting the neutral spec.

1. Read `.specify/feature.json`; load `plan.md` (per-group framework) and
   `tasks.md`. Load `.specify/extensions/qa/qa-config.yml` if present.

2. **Run each group with its framework's runner:**
   - `robot` → `robot <suite>`
   - `playwright` (py) → `pytest`; (ts) → `npx playwright test`
   - `cypress` → `npx cypress run`; `selenium`/`appium` → their runner
   Capture pass/fail per test, keyed back to `REQ-NNN`.

3. **Triage failures by layer:**
   - **API/contract failures** → likely a contract mismatch or assertion drift.
     Report the request/response diff; do not touch the app.
   - **UI/web failures** → drive the browser (driver chosen as in
     `speckit.qa.bind-locators`). For each failing test:
     - Navigate to the route and reproduce the step.
     - Capture **evidence** per config: screenshot, DOM snapshot, console
       errors (and network if enabled).
     - Classify the cause: **selector drift** (element moved/renamed →
       re-bind via `speckit.qa.bind-locators`), **timing** (needs an explicit
       wait/auto-wait), **real app bug** (the app misbehaves), or **bad
       expectation** (test asserts the wrong thing).

4. **Propose the minimal fix** for each, scoped to the right place:
   - selector drift → update the locator file only;
   - timing → adjust the wait in the test, not the data;
   - real app bug → file it as a finding with evidence (do not paper over it in
     the test);
   - bad expectation → flag for spec `clarify`, do not silently change behavior.
   Apply only fixes that are clearly mechanical (locator/timing); leave app
   bugs and expectation changes for human confirmation.

5. **Report**: per-`REQ` pass/fail, the cause and disposition of each failure,
   evidence paths, and any requirements now blocked by a real app bug.
