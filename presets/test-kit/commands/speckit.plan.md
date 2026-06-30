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
   - **Source under test (unit/integration groups).** Declare
     `source_under_test:` - the module / package / file paths whose code these
     tests exercise. `implement` reads and analyzes that source (signatures,
     types, branches) to generate tests against the real code API. Required for
     unit/integration groups; omit for API/UI.
   - **API contract source (optional, API groups).** Declare `contract_source:`
     when available - an OpenAPI/Swagger doc (file or URL) or the route/handler
     source code. `implement` reads it to build the real contract instead of
     relying only on the spec's prose. Omit to build from the spec.
   - **Fixtures, mocks, setup/teardown.** What is shared, what is per-test.
   - **Test data.** Named data sets in a dedicated data file - never inline.
   - **Locators / structural identifiers.** For the API layer this is base URLs,
     endpoints, headers - kept in a config/data file, not in tests.
   - **App-access strategy.** For API/contract: none required (work from the
     contract). UI/web is generated **only if you explicitly mark a group as UI
     here** - never inferred downstream. When you do, declare a reachable
     **URL** (`base_url` / route, local or remote): that lets `implement` do the
     integrated single-pass flow (navigate -> read DOM -> generate correct
     locators inline). If you cannot give a URL at plan time, `implement` leaves
     `__BIND__` placeholders and the `qa` extension's `speckit.qa.bind-locators`
     resolves them later (the fallback).

4. Do not write framework code here. Output is a plan, not tests.
