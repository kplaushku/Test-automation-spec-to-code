<div align="center">
    <img src="./media/logo.svg" alt="Specto logo" width="160" height="160"/>
    <h1>🧪 Specto</h1>
    <h3><em>Generate executable, multi-framework test suites from hand-written requirements.</em></h3>
</div>

<p align="center">
    <strong>A spec-driven test automation toolkit. You write requirements in natural
    language; Specto turns them into runnable tests in the framework you
    pick at planning time — Robot Framework, Playwright, Cypress, Selenium, or
    Appium.</strong>
</p>

---

## What this is

Specto adapts the spec-driven workflow to **test generation**. The same
chain of commands you'd use to spec software now produces tests:

| Command | Meaning here |
|---|---|
| `constitution` | Test strategy: allowed frameworks + default, levels, naming, coverage thresholds, flaky definition |
| `specify` | What to test, framework-neutral: Given/When/Then, preconditions, inputs, expected output, error cases |
| `clarify` | Block vague requirements before generating useless tests |
| `plan` | Test plan: framework choice per group, suite structure, fixtures, mocks, test data, app-access strategy |
| `tasks` | Neutral list of test cases to implement, with dependencies and parallel markers |
| `implement` | Generate code in the chosen framework, via a per-framework **adapter** |
| `analyze` | Spec-to-test coverage: which requirements have no test |
| `checklist` | Quality checklist on the tests themselves |

The core idea: **a test scenario is neutral with respect to the framework that
runs it.** "Given a logged-in user, when they open the cart, then they see the
added items" is the same scenario in Playwright, Cypress, or Robot. So the
scenario stays single and neutral, and only the final code generation is
framework-specific.

## Architecture

- **Neutral layers** — `constitution`, `specify`, `clarify`, `plan`, `tasks` —
  never mention a specific framework.
- **Framework layer** — `implement` only. It routes to an **adapter** per
  framework under
  [`presets/test-kit/templates/adapters/`](presets/test-kit/templates/adapters/).
- Adding a framework = adding an adapter. The neutral layers are untouched.
- The same spec can produce different framework outputs by changing only the
  choice in `plan`.

See [`presets/test-kit/README.md`](presets/test-kit/README.md) for the preset
details and [`extensions/traceability/`](extensions/traceability/) for the
requirement-to-test matrix command.

## Current scope (first increment)

- **Layers:** API / contract tests (no application access required).
- **Active adapters:** Robot Framework (RequestsLibrary) and Playwright
  (`request`).
- UI-web and mobile adapters come next, once the app-access strategy is decided.

## Status

Early. The neutral chain and the two API adapters are the first deliverable.

---

## Attribution

Specto is **based on [github/spec-kit](https://github.com/github/spec-kit),
released under the MIT License.** The original `LICENSE` and its copyright notice
are retained. New portions are licensed MIT (see [`LICENSE`](LICENSE)).

This is an **independent project**. It is **not** affiliated with, endorsed by,
or sponsored by GitHub, Inc., and does not use GitHub's name or marks beyond the
factual attribution above.
