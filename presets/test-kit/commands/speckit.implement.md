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
   - **UI locators - gated on an explicit upstream UI decision.** First check
     the plan: a group qualifies for live DOM access **only if** `constitution`
     and `plan` already declared it a UI/web group **and** gave an app-access
     strategy with a reachable URL (`base_url` / route, local or remote). The
     user must have chosen UI testing in the earlier steps - never infer it here.
     - **If UI was chosen and a URL is available** (and a browser driver exists:
       claude-in-chrome / claude-preview / computer-use, per `qa-config.yml`),
       do the **integrated single-pass flow**: navigate to the declared URL (or
       localhost), read the DOM / accessibility tree for each route the tasks
       touch, then generate each UI test in **one pass with correct locators
       inline** - semantic (role / text / label) preferred, structural derived
       from the real DOM (`data-testid` > role+name > stable `id` > minimal CSS).
     - **Otherwise** (UI not chosen upstream, no URL/app-access declared, or no
       browser driver) **do not navigate**: emit structural locators as
       `__BIND__:<name>` placeholders for `speckit.qa.bind-locators` to resolve
       later. Semantic locators from the spec are still written inline.
     - **Never start a browser for API/contract or unit groups, and never
       navigate when UI testing was not decided in `plan`.**
   - **Unit/integration - read the real source.** For unit/integration groups,
     do not write tests against an imagined API. The plan declares
     `source_under_test` (the module / package / file paths). Before generating:
     - **Read and analyze that source**: resolve the real import paths, the
       function / method / class **signatures**, parameter and return **types**,
       raised exceptions, and the branches an edge case must hit. Use the actual
       names and arities - never invent a signature.
     - **Generate tests against the real code API**: correct imports, real call
       signatures, and assertions tied to the spec's expected output. Cover the
       error/edge cases the spec names by exercising the real branches/exceptions.
     - If `source_under_test` is missing or a symbol cannot be found, **stop and
       report** the gap (ask for the path) rather than guessing the code's API.
     - No app access, no network - this is pure source analysis.
   - **API contract - prefer a declared source over prose.** If the plan declares
     an API `contract_source` (an OpenAPI/Swagger doc, or the route/handler source
     code), **read it** and build the expected endpoints, request shapes, status
     codes, and response fields from it, reconciled with the spec. Use the spec's
     prose only to fill what the source does not cover. With no source, build the
     contract from the spec's prose as before.
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
