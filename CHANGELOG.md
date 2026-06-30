# Changelog

All notable changes to Specto are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Specto is derived from [github/spec-kit](https://github.com/github/spec-kit)
(MIT); this changelog starts fresh from the fork and does not carry upstream
history.

## [Unreleased]

### Added
- Source-grounded generation: `implement` reads real code/contracts, not just
  prose. Unit/integration groups declare `source_under_test` and tests are
  generated against the analyzed source (signatures, types, branches). API groups
  may declare a `contract_source` (OpenAPI doc or route code) that `implement`
  reads to build the real contract. `specify` can also seed requirements by
  reading a provided source. Wired through plan, specify, implement, and the
  Robot/Playwright/Cypress adapters.
- `test-kit` preset: spec-driven **test generation**. Neutral commands
  (`constitution`, `specify`, `plan`, `tasks`) plus a framework-routing
  `implement`, and document scaffolds.
- Framework adapters under `presets/test-kit/templates/adapters/`, all with real
  rendering rules: Robot (API + Web UI via SeleniumLibrary + Python-keyword unit),
  Playwright (API + UI + pytest unit), Cypress (UI + `cy.request`), Selenium (Web
  UI), and Appium (native mobile).
- Unit/integration level (pytest and Robot Python keywords) and a `ci` extension
  (`speckit.ci.generate`) that emits GitHub Actions / GitLab CI running the suite,
  isolating quarantined flaky tests in a non-blocking job, and publishing the
  traceability + reliability artifacts.
- `traceability` extension: requirement-to-test matrix keyed on neutral
  `REQ-NNN` markers, framework-agnostic.
- `qa` extension (QA approach adapted from gstack, MIT): browser-driven
  `speckit.qa.bind-locators` (resolves structural UI locators against the live
  app), `speckit.qa.run` (run + evidence-based failure triage), and
  `speckit.qa.investigate` (single-failure root-cause). Closes the app-access
  gap for UI/web tests; wired into the plan app-access strategy, the UI
  adapters, and `implement` via `__BIND__:<name>` locator placeholders.
  Also `speckit.qa.verify` (confirm a test truly exercises its requirement;
  flags weak / false-green tests), `speckit.qa.review` (pre-landing quality
  review of the generated test code), and `speckit.qa.heal` (self-healing
  locators: re-derive a drifted selector from the live DOM and re-bind).
- `reliability` extension: `speckit.reliability.flake` (run N times, score, and
  quarantine flaky tests per the constitution's flaky definition) and
  `speckit.reliability.score` (a single 0-100 trust score from coverage,
  flakiness, assertion strength, and drift).
- `contract` extension: `speckit.contract.check` detects API contract drift -
  compares the live API's schema/responses against the spec's expectations and
  flags changed status codes, removed/changed fields, and new required fields,
  mapped back to each `REQ-NNN`.
- Worked, runnable example in `examples/test-kit-demo/` (Robot 3/3 + Playwright
  3/3 against a live API from one neutral spec).
- Original project branding: `media/logo.svg`, rebranded CLI tagline, rewritten
  governance files, README attribution to github/spec-kit (MIT).

### Notes
- See `VALIDATION.md` for acceptance-criteria evidence and known gaps.
