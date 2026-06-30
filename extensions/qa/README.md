# Live QA & Locator Binding extension

Brings browser-driven QA into Specto. Its main job is to **close the app-access
gap** that the project spec calls out for UI/web tests: generated UI tests carry
semantic locators (by text/role) inline, but structural locators are left as
placeholders. This extension opens the running app, reads the real DOM, and
resolves them - so the UI suite actually runs against the real selectors.

## Commands

| Command | What it does |
|---|---|
| `speckit.qa.bind-locators` | **Fallback / re-bind.** Open the live app, read the DOM, and fill `__BIND__` placeholders - used when `implement` ran without app access, or to re-bind after selector drift. (The default is the integrated single-pass flow inside `implement`.) |
| `speckit.qa.run` | Run the generated suite; for UI/web failures, capture screenshot + DOM + console evidence and propose a minimal, correctly-scoped fix. |
| `speckit.qa.investigate` | Deep root-cause of a single failing or flaky test: reproduce, isolate one variable, fix minimally. |
| `speckit.qa.verify` | Confirm a generated test truly exercises its requirement against real behavior - runs with observation on and falsifies it, flagging `weak` and `false-green` tests. |
| `speckit.qa.review` | Pre-landing quality review of the generated test code: separation, real assertions, flakiness, locator quality, edge-case coverage, reuse. Complements core `analyze`/`checklist`. |

## Browser drivers

UI/web commands need a browser. Any one of these satisfies them; the commands
probe in order and fall back (configurable in `qa-config.yml`):

1. `claude-in-chrome` MCP
2. `claude-preview` MCP
3. `computer-use` MCP
4. the gstack `browse` skill, if installed

API/contract testing needs **no** driver - this extension is inert for those
layers.

## How it wires into the pipeline

- `plan` declares whether a group is UI/web and its app-access strategy
  (including the URL). UI generation only happens when the plan chose it.
- **Default (integrated):** when the plan gives a UI group a reachable URL,
  `implement` itself navigates, reads the DOM, and writes correct locators
  inline in one pass - no separate binding step.
- **Fallback:** if `implement` had no app access, it leaves `__BIND__:<name>`
  placeholders, and `speckit.qa.bind-locators` resolves them later (also used to
  re-bind after selector drift).
- `speckit.qa.run` executes and QAs the result; a hook offers it right after
  `implement`.

## Attribution

The QA approach (live-browser dogfooding, evidence-first failure triage,
single-variable investigation, behavior verification, and pre-landing review) is
adapted from the **gstack** skills
[`browse`](https://github.com/garrytan/gstack/tree/main/browse),
[`qa`](https://github.com/garrytan/gstack/tree/main/qa),
[`investigate`](https://github.com/garrytan/gstack/tree/main/investigate),
[`verify`](https://github.com/garrytan/gstack/tree/main/verify), and
[`review`](https://github.com/garrytan/gstack/tree/main/review) by Garry Tan
(MIT). The concepts are re-implemented natively as Specto commands; no gstack
code is vendored. See [github.com/garrytan/gstack](https://github.com/garrytan/gstack).
