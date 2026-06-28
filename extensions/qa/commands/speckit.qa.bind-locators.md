---
description: Resolve structural UI locators from the live app via a browser, filling the locator file the adapters reference.
---

## User Input

```text
$ARGUMENTS
```

## Outline

This realizes Specto's **locator-binding** app-access strategy. Generated UI
tests carry *semantic* locators (by text/role, derived from the spec) inline,
but leave *structural* locators (css/xpath/test-id) as placeholders. This
command opens the running app, reads the real DOM, and fills those placeholders
so the UI suite actually runs. API/contract suites need none of this.

1. Read `.specify/feature.json` for the feature directory. Load
   `<feature_directory>/spec.md` (semantic intent) and the QA config
   `.specify/extensions/qa/qa-config.yml` (driver, `base_url`, `locator_file`).

2. **Pick a browser driver** from the config `driver` (default `auto`), probing
   availability in order and using the first present:
   - `claude-in-chrome` MCP (navigate, snapshot/accessibility tree, screenshot)
   - `claude-preview` MCP (preview_start, preview_snapshot, preview_inspect)
   - `computer-use` MCP (screenshot + click, last resort)
   - `gstack-browse` skill, if installed
   If none is available, stop and report: structural locators cannot be bound
   without app access; the semantic-only tests still run for elements with
   stable text/role.

3. **Collect the placeholders.** Scan the generated UI tests and the
   `locator_file` for unresolved structural-locator keys (e.g.
   `__BIND__:add-to-cart-button`). Each key has a semantic description from the
   spec (visible label, role, nearby text).

4. **Open the app and read the DOM.** Navigate to `base_url` plus the relevant
   route. Take an accessibility-tree / DOM snapshot. For each placeholder, find
   the element by its semantic description and derive the **most stable**
   structural locator, preferring in this order: `data-testid` / `data-test` →
   ARIA role + accessible name → unique stable `id` → minimal CSS path. Never
   emit brittle nth-child chains or auto-generated hashes when a stable
   attribute exists.

5. **Write only the locator file.** Put resolved structural locators in
   `<feature_directory>/<locator_file>`, keyed by the same semantic name. Do
   **not** inline them into tests and do **not** edit test logic or data. Record
   how each was found (testid/role/id/css) for review.

6. **Report**: bound vs still-unresolved placeholders (with a screenshot path as
   evidence for any element you could not locate), and which routes were
   visited. Suggest `speckit.qa.run` next.
