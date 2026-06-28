# Adapter: Selenium — PLANNED (not active)

Web-UI adapter over the WebDriver protocol. Not part of the current API-first
increment. To activate: implement the rendering rules below and add `selenium`
to the constitution's allowed frameworks.

- **Layers:** Web UI only. No API, no mobile, no unit.
- **Language:** cross-language (Python binding recommended to match the stack).
- **Requirement marker (neutral id → native):** a structured comment/marker on
  each test (e.g. `# REQ: REQ-001`) or a pytest marker when run under pytest.
- **Separation:** logic in test methods; data in a data file; locators in a Page
  Object / locators module — never inline selectors.
- **UI note:** always requires an app-access strategy (MCP, source, or
  locator-binding) — Selenium has no API layer to fall back on.
- **Relation:** shares the WebDriver protocol with Appium; Appium is its mobile
  counterpart.
