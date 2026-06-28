# Test Kit preset

Spec-driven **test generation**. Neutral test scenarios in, executable tests out.
The framework is chosen at plan time, never hard-wired.

## Pipeline

```
constitution  →  specify  →  clarify  →  plan  →  tasks  →  implement
   (strategy)    (neutral)   (resolve)  (pick fw)  (neutral)  (per-adapter)
```

- **Neutral layers** — `constitution`, `specify`, `plan`, `tasks` — carry no
  framework syntax. (`clarify`, `analyze`, `checklist` are reused from core.)
- **Framework layer** — `implement` only — routes each test group to its
  adapter.

## Capability matrix

| Framework | Web UI | Mobile native | API | Unit/integr. | Language | Status |
|---|---|---|---|---|---|---|
| Robot Framework | via SeleniumLibrary | via AppiumLibrary | RequestsLibrary | Python keywords | keyword-driven / Python | **active (API)** |
| Playwright | yes | web emulation only | request | partial | TS/JS/Python/.NET/Java | **active (API)** |
| Cypress | yes | no | cy.request | partial | JS/TS | planned |
| Selenium | yes | no | no | no | cross-language | planned |
| Appium | no | iOS/Android | no | no | cross-language | planned |

Framework choice is bound to the **test level**: only Robot covers API+unit
comfortably; the others are UI or mobile. `plan` validates each group's choice
against this matrix and the constitution.

## Current scope

- **Level:** API / contract (no application access required).
- **Active adapters:** `robot`, `playwright`.
- UI-web and mobile adapters are stubbed under
  [`templates/adapters/`](templates/adapters/) and activate once the app-access
  strategy is decided.

## Requirement traceability

Every requirement has a neutral id `REQ-NNN` (defined in the constitution,
attached in `specify`, carried through `tasks`, and written by each adapter in
its native form — a Robot `[Tags]`, a Playwright marker/comment). The
[`traceability` extension](../../extensions/traceability/) reads these back into
a requirement-to-test matrix and flags uncovered requirements.

## App access (UI / mobile only)

API and unit need no app access. UI-web needs the DOM; mobile needs the element
tree. Three strategies, chosen in `plan` before any such test is generated:
**MCP** (drive the real app), **source** (feed the frontend/layout source), or
**locator-binding** (semantic locators in tests, structural ones resolved
separately). Semantic locators (by text/role) derived from visible labels in the
spec often render correctly without app access; only structural locators need
binding.

## Install

```
specify preset add test-kit --priority 10
```

The preset overrides the `constitution`, `specify`, `plan`, `tasks`, and
`implement` commands plus the `spec`/`plan`/`tasks` document scaffolds. Core
orchestration scripts are untouched.

## Adding a framework

Add an adapter directory under `templates/adapters/<framework>/` with an
`ADAPTER.md` (rendering rules + requirement-marker translation), declare it in
`preset.yml`, and add the framework to the constitution's allowed list. No
neutral layer changes.
