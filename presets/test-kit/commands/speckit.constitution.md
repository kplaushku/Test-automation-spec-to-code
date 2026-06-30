---
description: Create or update the test strategy (constitution) for this project.
---

## User Input

```text
$ARGUMENTS
```

## Outline

You are defining the **test strategy** that governs every later command. It is
framework-neutral except for declaring which frameworks are allowed.

1. Load `.specify/memory/constitution.md` if it exists; otherwise start fresh.

2. Produce `.specify/memory/constitution.md` covering:

   - **Allowed frameworks and default.** A list drawn from: `robot`,
     `playwright`, `cypress`, `selenium`, `appium`. Mark exactly one as the
     default. For this project's current scope the realistic set is `robot`
     and `playwright` (API layer). Record the default explicitly, e.g.
     `default_framework: robot`.
   - **Test levels in scope.** Any of: API/contract, unit/integration, UI web,
     mobile native. State which are active. All four have adapter support; API
     and unit need no app access, UI/mobile require an app-access strategy.
   - **Requirement identifiers.** Every requirement carries a stable neutral id
     of the form `REQ-NNN` (e.g. `REQ-001`). These ids are the link between
     spec and tests and MUST appear on every generated test. Define the scheme
     here.
   - **Naming conventions.** Suite, file, and test-case naming.
   - **Structure rule (non-negotiable).** Test logic, test data, and locators
     are always separated - never inline literals (URLs, payloads, selectors,
     credentials) inside a test case. Data lives in a data file; structural
     locators live in a locator file.
   - **Coverage thresholds.** Requirement coverage target (share of `REQ-*`
     that must have at least one test). Keep this distinct from code coverage.
   - **Flaky definition.** What counts as a flaky test and how it is handled.

3. Keep the document framework-neutral apart from the allowed-frameworks list.
   No framework-specific syntax, no selectors, no code.

4. Report what changed and which downstream commands are affected.
