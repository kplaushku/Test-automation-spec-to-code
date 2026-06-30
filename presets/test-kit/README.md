# Test Kit preset

Spec-driven **test generation**. Neutral test scenarios in, executable tests out.
The framework is chosen at plan time, never hard-wired.

## Pipeline

```
constitution  →  specify  →  clarify  →  plan  →  tasks  →  implement
   (strategy)    (neutral)   (resolve)  (pick fw)  (neutral)  (per-adapter)
```

- **Neutral layers** - `constitution`, `specify`, `plan`, `tasks` - carry no
  framework syntax. (`clarify`, `analyze`, `checklist` are reused from core.)
- **Framework layer** - `implement` only - routes each test group to its
  adapter.

## Capability matrix

| Framework | Web UI | Mobile native | API | Unit/integr. | Language | Status |
|---|---|---|---|---|---|---|
| Robot Framework | SeleniumLibrary | via AppiumLibrary | RequestsLibrary | Python keywords | keyword-driven / Python | **active (API + UI + unit)** |
| Playwright | yes | web emulation only | request | pytest unit | TS/JS/Python/.NET/Java | **active (API + UI + unit)** |
| Cypress | yes | no | cy.request | partial | JS/TS | **active (UI + API)** |
| Selenium | yes | no | no | no | cross-language | **active (UI)** |
| Appium | no | iOS/Android | no | no | cross-language | **active (mobile)** |

Framework choice is bound to the **test level**: only Robot covers API+unit
comfortably; the others are UI or mobile. `plan` validates each group's choice
against this matrix and the constitution.

## Current scope

- **Levels:** API / contract (no app access), unit / integration, and UI / web.
  Mobile (Appium) generation is codified; a live run needs a device/emulator.
- **Active adapters:** all five have real rendering rules -
  `robot` (API + UI + unit), `playwright` (API + UI + unit), `cypress` (UI + API),
  `selenium` (UI), `appium` (mobile).
- UI/mobile groups need an app-access strategy (a URL in the plan), realized by
  the `qa` extension; API and unit need none.

## Requirement traceability

Every requirement has a neutral id `REQ-NNN` (defined in the constitution,
attached in `specify`, carried through `tasks`, and written by each adapter in
its native form - a Robot `[Tags]`, a Playwright marker/comment). The
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

The **[`qa` extension](../../extensions/qa/)** realizes the locator-binding and
MCP strategies: `speckit.qa.bind-locators` opens the live app via a browser MCP,
reads the real DOM, and resolves the `__BIND__:<name>` placeholders that UI
adapters emit. `speckit.qa.run` then runs the suite and QAs UI failures with
screenshot/DOM evidence. This closes the app-access gap for UI/web tests.

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
