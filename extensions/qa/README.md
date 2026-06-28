# Live QA & Locator Binding extension

Brings browser-driven QA into Specto. Its main job is to **close the app-access
gap** that the project spec calls out for UI/web tests: generated UI tests carry
semantic locators (by text/role) inline, but structural locators are left as
placeholders. This extension opens the running app, reads the real DOM, and
resolves them - so the UI suite actually runs against the real selectors.

## Commands

| Command | What it does |
|---|---|
| `speckit.qa.bind-locators` | Open the live app via a browser, read the DOM/accessibility tree, fill the structural-locator file the adapters reference. Realizes the **locator-binding / MCP** app-access strategy. |
| `speckit.qa.run` | Run the generated suite; for UI/web failures, capture screenshot + DOM + console evidence and propose a minimal, correctly-scoped fix. |
| `speckit.qa.investigate` | Deep root-cause of a single failing or flaky test: reproduce, isolate one variable, fix minimally. |

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

- `plan` declares the app-access strategy. For UI/web, the strategy is
  `locator-binding`, realized by `speckit.qa.bind-locators`.
- `implement` generates UI tests with semantic locators inline and structural
  ones as `__BIND__:<name>` placeholders in the locator file.
- `speckit.qa.bind-locators` resolves the placeholders against the live app.
- `speckit.qa.run` executes and QAs the result; a hook offers it right after
  `implement`.

## Attribution

The QA approach (live-browser dogfooding, evidence-first failure triage,
single-variable investigation) is adapted from the **gstack** skills
[`browse`](https://github.com/garrytan/gstack/tree/main/browse),
[`qa`](https://github.com/garrytan/gstack/tree/main/qa), and
[`investigate`](https://github.com/garrytan/gstack/tree/main/investigate) by
Garry Tan (MIT). The concepts are re-implemented natively as Specto commands;
no gstack code is vendored. See [github.com/garrytan/gstack](https://github.com/garrytan/gstack).
