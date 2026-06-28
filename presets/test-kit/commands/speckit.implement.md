---
description: Generate test code in the framework chosen in the plan, via the matching adapter.
---

## User Input

```text
$ARGUMENTS
```

## Outline

This is the **only framework-specific command.** It turns neutral tasks into
runnable tests by routing each group to its framework's adapter. The neutral
artifacts (`spec.md`, `plan.md`, `tasks.md`) are inputs only - never edit them.

1. Read `.specify/feature.json` for the feature directory.

2. **Load context**: `.specify/memory/constitution.md`,
   `<feature_directory>/spec.md`, `<feature_directory>/plan.md`,
   `<feature_directory>/tasks.md`.

3. **Resolve the framework per task.** For each task, find its group in
   `plan.md` and read that group's `framework:` value. This selects the adapter.

4. **Load the matching adapter** rules:
   - `robot` → `adapter-robot`
     (`presets/test-kit/templates/adapters/robot/ADAPTER.md`)
   - `playwright` → `adapter-playwright`
     (`presets/test-kit/templates/adapters/playwright/ADAPTER.md`)
   Refuse any framework not allowed by the constitution.

5. **Generate tests** following the adapter, honoring three rules from the
   constitution:
   - **Separation.** Test logic, test data, and locators/config live in separate
     files. No inline URLs, payloads, selectors, or credentials.
   - **UI locators.** For UI/web/mobile groups, write *semantic* locators
     (text/role from the spec) inline, but emit *structural* locators as
     `__BIND__:<name>` placeholders in the locator file. The `qa` extension's
     `speckit.qa.bind-locators` resolves them against the live app. Skip this
     for API/contract groups.
   - **Requirement marker.** Every generated test carries its `REQ-NNN` id,
     written in that framework's native way (the adapter specifies how - a Robot
     `[Tags]` entry, a Playwright tag/annotation). This is what the traceability
     command reads.
   - **Suite layout.** Follow the structure declared in `plan.md`.

6. Mark each completed task `- [ ]` → `- [x]` in `tasks.md`. Halt and report on
   failure.

7. **Validate.** Confirm every task is implemented, every test carries a
   `REQ-NNN` marker, and data/locators are externalized. Report a per-framework
   summary and which requirements are now covered.
