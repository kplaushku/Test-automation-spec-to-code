# QA UI demo - locator binding

Illustrates how the **`qa` extension** closes the app-access gap for UI tests.
Unlike `test-kit-demo` (API, fully runnable here with no app), this UI flow needs
a running app + a browser MCP to execute, so it is shown as **artifacts** plus
the binding steps.

## The three states of a structural locator

1. **Generated** (`implement`): the UI test uses semantic locators inline
   (`get_by_label("Email")`, `get_by_role("button", name="Log in")`) and
   references structural ones by name from `config/locators.generated.json`,
   which starts as a placeholder:

   ```json
   { "dashboard_greeting": "__BIND__:dashboard-greeting" }
   ```

2. **Bound** (`speckit.qa.bind-locators`): the command opens the live app via a
   browser MCP, reads the DOM, finds the greeting element, and rewrites the
   placeholder with the most stable structural locator it can derive:

   ```json
   { "dashboard_greeting": "[data-testid='dashboard-greeting']" }
   ```

   (Preference order: data-testid -> role+name -> stable id -> minimal CSS.)

3. **Run + QA** (`speckit.qa.run`): runs the suite; on a UI failure it captures
   a screenshot + DOM + console as evidence and classifies the cause (selector
   drift -> re-bind; timing -> wait; real bug -> file it; bad expectation ->
   `clarify`).

## Why this is the smart part

The spec's hardest open problem was UI/mobile **app access** - without it the
agent guesses selectors and ships tests that look right but do not run. Here the
agent writes everything it *can* know from the spec (semantic locators), and only
the genuinely unknowable structural locators are deferred to a single,
browser-backed binding step. Most of the test is correct before any app access;
binding is a small, isolated, reviewable diff.

## To run for real

1. Point `qa-config.yml` `base_url` at your running app.
2. Ensure a browser MCP is available (claude-in-chrome / claude-preview /
   computer-use), or the gstack `browse` skill.
3. `speckit.qa.bind-locators` then `speckit.qa.run`.
