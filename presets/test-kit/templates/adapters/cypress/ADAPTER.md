# Adapter: Cypress - Web UI + API

Rendering rules that turn a neutral test case (from `tasks.md`) into Cypress
tests. Two layers: **Web UI** (the default) and **API** (`cy.request`).

## Capabilities

| Web UI | Mobile | API | Unit/integration | Language |
|--------|--------|-----|------------------|----------|
| yes | no | `cy.request` | partial | JS / TS |

## File layout

```
cypress/
  e2e/<group>.cy.js        # one spec per group
  fixtures/<group>.json    # named test data - no inline literals
  support/
    locators/<group>.js    # structural locators (bound), never inline in tests
    commands.js            # shared custom commands (test logic helpers)
cypress.config.js          # baseUrl, env, retries
```

## Requirement marker (neutral id -> native)

A Cypress test tag (via `@cypress/grep`) plus a structured comment, so the
traceability command can grep either form:

```js
it("creates an order", { tags: ["REQ-001"] }, () => { /* REQ: REQ-001 */ });
```

## Separation rules

- **Logic** in `e2e/*.cy.js` and `support/commands.js`.
- **Data** in `fixtures/*.json`, loaded with `cy.fixture(...)`. Never inline a
  payload or expected body.
- **Config/locators:** `baseUrl` in `cypress.config.js`; structural locators in
  `support/locators/*.js`.

## Locator strategy (semantic inline, structural from the live DOM)

- **Semantic inline** - prefer Testing-Library-style queries
  (`cy.findByRole`, `cy.findByLabelText`) or `cy.contains(...)`, derived from the
  spec's visible labels.
- **Structural** - integrated when the plan gives a URL (`implement` reads the
  DOM and writes the locator inline; prefer `data-cy`/`data-testid` > role+name
  > stable id > minimal CSS). Otherwise a `__BIND__:<name>` placeholder in the
  locator module, resolved by `speckit.qa.bind-locators`.

## Rendering a neutral UI case

For `T010 [REQ-010] login - successful login shows dashboard`:

```js
import { L } from "../support/locators/login";

describe("login", () => {
  it("successful login shows dashboard", { tags: ["REQ-010"] }, () => {
    // REQ: REQ-010
    cy.fixture("login").then((creds) => {
      cy.visit("/login");
      cy.findByLabelText("Email").type(creds.valid.email);
      cy.findByLabelText("Password").type(creds.valid.password);
      cy.findByRole("button", { name: "Log in" }).click();
      cy.get(L.dashboardGreeting).should("be.visible"); // bound from the live DOM
    });
  });
});
```

Rely on Cypress retry-ability and `should(...)` assertions; never `cy.wait(ms)`
on a fixed timer (flaky per the constitution).

## API case (`cy.request`)

```js
it("create order returns 201", { tags: ["REQ-001"] }, () => {
  // REQ: REQ-001
  cy.fixture("orders").then((d) =>
    cy.request("POST", "/orders", d.valid_order).its("status").should("eq", 201));
});
```

## Run

```
npm i -D cypress @cypress/grep @testing-library/cypress
npx cypress run
```
