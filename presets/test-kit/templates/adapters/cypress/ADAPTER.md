# Adapter: Cypress - PLANNED (not active)

Web-UI / API (`cy.request`) adapter. Not part of the current API-first increment
with Robot + Playwright. To activate: implement the rendering rules below and add
`cypress` to the constitution's allowed frameworks.

- **Layers:** Web UI, API (`cy.request`). No mobile.
- **Language:** JS / TS.
- **Requirement marker (neutral id → native):** Cypress test tags via
  `@cypress/grep` (e.g. `it('...', { tags: ['REQ-001'] }, ...)`) plus a
  `// REQ: REQ-001` comment for grep-based traceability.
- **Separation:** logic in `*.cy.js`; data in `cypress/fixtures/*.json`;
  config/locators in `cypress.config.js` / a locators module.
- **UI note:** requires an app-access strategy before generating UI tests
  (see the preset README). API tests via `cy.request` do not.
