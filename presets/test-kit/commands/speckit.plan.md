---
description: Create the test plan, choosing the framework per group, and store it in plan.md.
---

## User Input

```text
$ARGUMENTS
```

## Outline

This is the **only neutral command where a framework is chosen.** The spec stays
untouched; the choice lives here so the same spec can target different frameworks.

1. Read `.specify/feature.json` for the feature directory.

2. **Load context**: `.specify/memory/constitution.md` and
   `<feature_directory>/spec.md`. Refuse to proceed if the spec still contains
   `[NEEDS CLARIFICATION]` markers - run `clarify` first.

3. Resolve the `plan-template` and write `<feature_directory>/plan.md` covering:

   - **Test groups.** Partition the `REQ-*` requirements into coherent groups
     (e.g. by endpoint or capability).
   - **Framework per group.** For each group pick one framework from the
     constitution's allowed list, defaulting to its `default_framework`. Record
     it as `framework: <id>`. Different groups MAY use different frameworks.
     Validate every choice against the constitution - reject any framework not
     allowed, and any choice whose capabilities don't fit the test level (see
     the capability matrix in the preset README).
   - **Suite structure.** Directory layout, file-per-group mapping.
   - **Fixtures, mocks, setup/teardown.** What is shared, what is per-test.
   - **Test data.** Named data sets in a dedicated data file - never inline.
   - **Locators / structural identifiers.** For the API layer this is base URLs,
     endpoints, headers - kept in a config/data file, not in tests.
   - **App-access strategy.** For API/contract: none required (work from the
     contract). For UI/mobile (future): declare MCP, source, or locator-binding
     before any such test is generated.

4. Do not write framework code here. Output is a plan, not tests.
