---
description: Build a requirement-to-test matrix from the spec and the generated tests, framework-neutral.
---

## User Input

```text
$ARGUMENTS
```

## Outline

Produce a **requirement-to-test traceability matrix**. The mechanism is neutral:
it keys on the `REQ-NNN` identifier that every adapter writes in its framework's
native form. Do not assume a single framework - a project may mix several.

1. Read `.specify/feature.json` for the feature directory.

2. **Collect requirements.** Parse `<feature_directory>/spec.md` for every
   `REQ-NNN` id and its short name. This is the authoritative requirement set.

3. **Collect test markers.** Scan the generated test tree for `REQ-NNN`
   occurrences, in any of these native forms (search them all):
   - Robot Framework: `[Tags]    REQ-NNN`
   - Playwright (Python): `@pytest.mark.req("REQ-NNN")` or `# REQ: REQ-NNN`
   - Playwright (TS) / Cypress: `tag: '@REQ-NNN'`, `tags: ['REQ-NNN']`, or
     `// REQ: REQ-NNN`
   - Selenium / Appium: `# REQ: REQ-NNN` or a runner marker
   For each hit, record requirement id → test file + test name + framework.

4. **Build the matrix.** Write
   `<feature_directory>/traceability.md` containing:

   | Requirement | Name | Tests | Framework(s) | Status |
   |-------------|------|-------|--------------|--------|
   | REQ-001 | create order | tests/test_orders.py::test_create_order_returns_201 | playwright | ✅ |
   | REQ-002 | ... | - | - | ❌ uncovered |

5. **Flag gaps both ways:**
   - **Uncovered requirements:** any `REQ-NNN` in the spec with no test. List
     them explicitly - this is the headline output.
   - **Orphan markers:** any `REQ-NNN` found in tests but absent from the spec
     (typo or stale id).

6. **Summary line:** `N/M requirements covered (X%)`, compared against the
   coverage threshold in `.specify/memory/constitution.md`. State pass/fail
   against that threshold. Coverage here is **requirement coverage**, not code
   coverage - keep them distinct.

7. Do not modify spec, plan, tasks, or test files. This command only reads them
   and writes `traceability.md`.
