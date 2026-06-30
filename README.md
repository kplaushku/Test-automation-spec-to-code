<div align="center">
    <img src="./media/logo.svg" alt="Specto logo" width="150" height="150"/>
    <h1>Specto</h1>
    <h3><em>From one spec, executable tests in every framework.</em></h3>
    <p>
        <img src="https://img.shields.io/badge/license-MIT-3fb950" alt="MIT License"/>
        <img src="https://img.shields.io/badge/python-3.11%2B-3776AB" alt="Python 3.11+"/>
        <img src="https://img.shields.io/badge/frameworks-Robot%20%7C%20Playwright%20%7C%20Cypress%20%7C%20Selenium%20%7C%20Appium-1f9d8b" alt="Frameworks"/>
        <img src="https://img.shields.io/badge/status-alpha-orange" alt="Status: alpha"/>
    </p>
</div>

> **Specto turns hand-written requirements into runnable, multi-framework test suites.**
> You describe *what* to test in plain language; Specto plans the suite, picks the
> framework, and generates the test code - with traceability back to every
> requirement. The scenario is written once and stays framework-neutral; only the
> final code generation is framework-specific.

---

## Table of contents

- [Why Specto](#why-specto)
- [How it works](#how-it-works)
- [Quickstart](#quickstart)
- [Example: one spec, two frameworks](#example-one-spec-two-frameworks)
- [UI testing: tests from the live DOM](#ui-testing-tests-from-the-live-dom)
- [Supported frameworks](#supported-frameworks)
- [Extensions](#extensions)
- [Architecture](#architecture)
- [Project structure](#project-structure)
- [Roadmap](#roadmap)
- [Attribution and license](#attribution-and-license)

---

## Why Specto

Writing automated tests by hand is slow, and the same scenario gets rewritten for
every framework. Specto starts from the artifact you should be writing anyway -
clear requirements - and treats them as the single source of truth:

- **Write the scenario once.** "Given a logged-in user, when they open the cart,
  then they see the added items" is the same test in Playwright, Cypress, or
  Robot. Specto keeps it neutral and generates the framework code.
- **Switch frameworks by changing one line.** Re-target a suite from Robot to
  Playwright by editing the plan, not the spec.
- **Every test is traceable.** Each generated test carries the id of the
  requirement it verifies, so coverage gaps are visible, not guessed.
- **Real selectors, not guesses.** For UI tests, Specto reads the live DOM and
  writes correct locators instead of inventing them.

## How it works

Specto reuses a proven spec-driven command chain. The first four commands are
**framework-neutral**; the framework is chosen in `plan` and realized only in
`implement`.

```
constitution -> specify -> clarify -> plan -> tasks -> implement
   strategy      neutral    resolve   pick fw  neutral   per-adapter
                                                          + traceability + qa
```

| Command | What it does in Specto |
|---|---|
| `/speckit.constitution` | Test strategy: allowed frameworks + default, levels, naming, coverage thresholds, flaky definition |
| `/speckit.specify` | *What* to test, framework-neutral: precondition -> input -> object -> expected output -> error cases (Given/When/Then) |
| `/speckit.clarify` | Blocks vague requirements before any test is generated |
| `/speckit.plan` | Test plan: framework per group, suite structure, fixtures, mocks, test data, and (for UI) the app URL |
| `/speckit.tasks` | Neutral list of test cases, each tagged with its requirement id |
| `/speckit.implement` | Generates the test code via the chosen framework's **adapter** |
| `/speckit.traceability.matrix` | Builds a requirement-to-test matrix and flags uncovered requirements |
| `/speckit.qa.*` | Runs, verifies, reviews, and binds UI locators against the live app |

## Quickstart

**Requirements:** Python 3.11+, an AI coding agent (Claude Code, Copilot, Gemini,
etc.), and [`uv`](https://docs.astral.sh/uv/) (recommended).

```bash
# 1. Get Specto
git clone https://github.com/kplaushku/Test-automation-spec-to-code.git
cd Test-automation-spec-to-code
uv sync                       # or: pip install -e .

# 2. Scaffold a test project with the test-kit preset
specify init my-tests --preset test-kit --integration claude

# 3. Add the extensions you want
cd my-tests
specify extension add traceability
specify extension add qa
```

Then, inside your AI coding agent, run the Specto commands in order:

```text
/speckit.constitution   frameworks: robot + playwright; levels: API; coverage 100%
/speckit.specify        the requirements you want to test, in plain language
/speckit.clarify        answer anything ambiguous
/speckit.plan           choose the framework per group
/speckit.tasks          generate the neutral test-case list
/speckit.implement      generate the runnable tests
/speckit.traceability.matrix   confirm every requirement is covered
```

## Example: one spec, two frameworks

This is the worked, **runnable** demo in
[`examples/test-kit-demo/`](examples/test-kit-demo/). One neutral spec produces a
green suite in **both** Robot Framework and Playwright, against a live public API.

**1. The neutral spec** (`spec.md`, framework-agnostic):

```markdown
### REQ-001 - fetch existing post
- Precondition: the API is reachable; post id 1 exists.
- Input: GET /posts/1
- Expected output: status 200; body has id = 1 and non-empty title and body.
```

**2. The neutral task** (`tasks.md`) - the same line drives both frameworks:

```text
- [ ] T001 [REQ-001] posts - fetch existing post returns 200 with fields
```

**3. `implement` renders it per framework.** The only difference is the
`framework:` line in the plan:

<table>
<tr><th>Robot Framework (<code>plan.robot.md</code>)</th><th>Playwright (<code>plan.playwright.md</code>)</th></tr>
<tr><td>

```robotframework
Fetch Existing Post Returns 200 With Fields
    [Tags]    REQ-001
    ${resp}=    GET On Session    api    /posts/1
    Status Should Be    200    ${resp}
    Should Be Equal As Integers
    ...    ${resp.json()}[id]    1
```

</td><td>

```python
@pytest.mark.req("REQ-001")
def test_fetch_existing_post(api):  # REQ: REQ-001
    resp = api.get("/posts/1")
    assert resp.status == 200
    body = resp.json()
    assert body["id"] == 1
```

</td></tr>
</table>

Note the requirement id (`REQ-001`) is carried natively in each framework - a
Robot `[Tags]` entry, a Playwright marker + comment - and test data, URLs, and
headers live in separate config/data files, never inline.

**4. Traceability** (`/speckit.traceability.matrix`) reads both suites and
produces a neutral matrix:

| Requirement | Robot test | Playwright test | Status |
|---|---|---|---|
| REQ-001 | `Fetch Existing Post Returns 200 With Fields` | `test_fetch_existing_post` | ✅ |

**5. Result** - both suites run green against the live API:

```text
Robot Framework  ->  3 tests, 3 passed, 0 failed
Playwright       ->  3 passed
Requirement coverage: 3/3 (100%)
```

## UI testing: tests from the live DOM

For UI/web tests, guessing selectors produces tests that look right but do not
run. Specto solves this with an **integrated, gated flow**:

- **You choose UI testing upstream.** A browser is used **only** when `plan`
  explicitly marks a group as UI/web and gives a reachable URL. API and unit
  groups never start a browser.
- **`implement` reads the real DOM.** When a UI group has a URL, `implement`
  navigates to it (local or remote), reads the DOM / accessibility tree, and
  writes **correct locators inline in one pass** - semantic locators
  (`get_by_role`, `get_by_label`, `get_by_text`) preferred, structural ones
  derived from the live page (`data-testid` > role+name > stable id > minimal CSS).
- **Graceful fallback.** No URL at plan time? `implement` leaves `__BIND__`
  placeholders, and the `qa` extension's `/speckit.qa.bind-locators` resolves
  them later (also used to re-bind after selectors drift).

```python
# Generated UI test - real Playwright API, real locators from the live DOM
@pytest.mark.req("REQ-010")
def test_successful_login_shows_dashboard(page, base_url, creds):  # REQ: REQ-010
    page.goto(f"{base_url}/login")
    page.get_by_label("Email").fill(creds["valid"]["email"])
    page.get_by_label("Password").fill(creds["valid"]["password"])
    page.get_by_role("button", name="Log in").click()
    expect(page.locator(L["dashboard_greeting"])).to_be_visible()
```

See [`examples/qa-ui-demo/`](examples/qa-ui-demo/) for the full flow.

## Supported frameworks

The framework is bound to the **test level** - only Robot covers API + unit
comfortably; the others are UI or mobile. `plan` validates each choice against
this matrix.

| Framework | Web UI | Mobile | API | Unit | Language | Status |
|---|---|---|---|---|---|---|
| **Robot Framework** | via SeleniumLibrary | via AppiumLibrary | RequestsLibrary | Python keywords | keyword-driven / Python | **active (API)** |
| **Playwright** | yes | web emulation | request | partial | TS / JS / Python / .NET / Java | **active (API + UI)** |
| Cypress | yes | no | `cy.request` | partial | JS / TS | planned |
| Selenium | yes | no | no | no | cross-language | planned |
| Appium | no | iOS / Android | no | no | cross-language | planned |

Adding a framework means adding one **adapter** under
[`presets/test-kit/templates/adapters/`](presets/test-kit/templates/adapters/) -
the neutral layers never change.

## Extensions

| Extension | Commands | Purpose |
|---|---|---|
| **[traceability](extensions/traceability/)** | `/speckit.traceability.matrix` | Requirement-to-test matrix from the spec + generated tests; flags uncovered requirements. Framework-neutral. |
| **[qa](extensions/qa/)** | `/speckit.qa.bind-locators`, `.run`, `.verify`, `.investigate`, `.review` | Browser-driven QA: bind UI locators from the live DOM, run suites with screenshot/DOM evidence, verify tests truly exercise their requirement, root-cause failures, and review test quality before landing. |

## Architecture

```
Neutral layers (no framework anywhere)
   constitution -> specify -> clarify -> plan -> tasks
                                          |
                                          | framework chosen here
                                          v
Framework layer
   implement --> adapter (robot | playwright | cypress | selenium | appium)
                                          |
                                          v
   traceability matrix  +  qa (live DOM, run, verify, review)
```

- **Neutral layers** never mention a framework. The scenario is portable.
- **Adapters** isolate everything framework-specific (syntax, file layout,
  locator strategy, how a requirement id is written natively).
- **Separation is enforced:** test logic, test data, and locators always live in
  separate files - no inline URLs, payloads, selectors, or credentials.

## Project structure

```
.
├── presets/test-kit/            # the test-generation preset
│   ├── commands/                # constitution, specify, plan, tasks, implement
│   └── templates/
│       ├── spec/plan/tasks      # neutral document scaffolds
│       └── adapters/            # one folder per framework
├── extensions/
│   ├── traceability/            # requirement-to-test matrix
│   └── qa/                      # live-DOM QA, run, verify, review
├── examples/
│   ├── test-kit-demo/           # one spec -> Robot + Playwright (API, runnable)
│   └── qa-ui-demo/              # the UI locator-binding flow
├── src/specify_cli/             # the CLI engine (specify)
└── LICENSE  README.md  VALIDATION.md
```

## Roadmap

- ✅ Neutral pipeline + Robot/Playwright API adapters (runnable demo)
- ✅ Traceability matrix and browser-driven QA extension
- ✅ Playwright UI layer with live-DOM locator generation
- ⏳ Robot UI (SeleniumLibrary) and Cypress/Selenium/Appium adapters
- ⏳ Unit/integration level and CI recipes

See [`VALIDATION.md`](VALIDATION.md) for acceptance-criteria evidence.

## Attribution and license

Specto is released under the **[MIT License](LICENSE)** and is **based on
[github/spec-kit](https://github.com/github/spec-kit)** (MIT). The original
license and copyright notice are retained; new portions are MIT.

This is an **independent project**. It is not affiliated with, endorsed by, or
sponsored by GitHub, Inc. The browser-driven QA approach is adapted from the
[gstack](https://github.com/garrytan/gstack) skills (Garry Tan, MIT); no gstack
code is vendored.
