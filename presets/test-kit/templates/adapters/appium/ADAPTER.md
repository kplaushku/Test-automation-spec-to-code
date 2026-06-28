# Adapter: Appium - PLANNED (not active)

Mobile-native adapter (iOS, Android) over the WebDriver protocol. Not part of the
current API-first increment. To activate: implement the rendering rules below and
add `appium` to the constitution's allowed frameworks.

- **Layers:** Mobile native only. No web, no API, no unit.
- **Language:** cross-language (WebDriver clients).
- **Requirement marker (neutral id → native):** a structured comment/marker on
  each test (e.g. `# REQ: REQ-001`) or a runner marker (pytest/JUnit).
- **Separation:** logic in test methods; data in a data file; element locators in
  a screen-object / locators module - never inline.
- **App-access note:** requires access to the app's element tree (accessibility
  ids / source) before generating tests, otherwise locators are guessed. Emit
  `__BIND__:<name>` placeholders; binding the mobile element tree is the
  device-driver counterpart of the `qa` extension's `speckit.qa.bind-locators`
  (browser-based today; a device driver is future work).
- **Relation:** Appium is the mobile extension of the same WebDriver model as
  Selenium.
