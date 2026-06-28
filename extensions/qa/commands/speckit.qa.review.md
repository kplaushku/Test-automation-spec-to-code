---
description: Pre-landing quality review of the generated tests - reuse, separation, assertions, flakiness, coverage.
---

## User Input

```text
$ARGUMENTS  (optional: a path/group to scope the review)
```

## Outline

Adapted from gstack's review flow. A quality-only pass over the **generated test
code** before it lands. It does not hunt for app bugs (that is `speckit.qa.run`)
- it reviews the tests themselves against the constitution.

1. Resolve the feature directory via `.specify/feature.json`; load
   `.specify/memory/constitution.md`, `spec.md`, `plan.md`, and the generated
   tests (scoped by `$ARGUMENTS` if given).

2. **Review each test against these checks:**
   - **Separation.** No inline URLs, payloads, selectors, or credentials -
     data in the data file, structural locators in the locator file, config in
     config. Flag any literal that belongs elsewhere.
   - **Requirement marker.** Every test carries a `REQ-NNN` marker in the
     framework's native form (the traceability mechanism depends on it).
   - **Real assertions.** Each test asserts the specific output the requirement
     names - no empty bodies, no tautologies, no asserting only HTTP 200 when
     the requirement names fields.
   - **Flakiness.** No bare sleeps or race-prone waits; prefer auto-wait /
     explicit conditions. Flag patterns matching the constitution's flaky
     definition.
   - **Locators.** Prefer semantic (text/role) over brittle structural; no
     nth-child chains or generated-hash selectors where a stable one exists.
   - **Coverage.** Each requirement's error/edge cases (from `spec.md`) have a
     test, not just the happy path. List uncovered cases.
   - **Reuse.** No copy-pasted setup that belongs in a fixture/keyword.

3. **Produce findings** ordered by severity, each with file:line and a concrete
   fix. Apply only the mechanical, unambiguous ones (move a literal to the data
   file, add a missing `REQ` marker); leave assertion/coverage changes for human
   confirmation.

4. **Report** a pass/fail summary against the constitution's thresholds and the
   list of findings. This complements core `analyze` (spec-to-test coverage) and
   `checklist` (requirements quality) by reviewing the test code itself.
