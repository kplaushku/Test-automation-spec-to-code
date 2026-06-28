# Changelog

All notable changes to Specto are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

Specto is derived from [github/spec-kit](https://github.com/github/spec-kit)
(MIT); this changelog starts fresh from the fork and does not carry upstream
history.

## [Unreleased]

### Added
- `test-kit` preset: spec-driven **test generation**. Neutral commands
  (`constitution`, `specify`, `plan`, `tasks`) plus a framework-routing
  `implement`, and document scaffolds.
- Framework adapters under `presets/test-kit/templates/adapters/`: Robot
  Framework and Playwright active for the API/contract layer; Cypress, Selenium,
  and Appium stubbed.
- `traceability` extension: requirement-to-test matrix keyed on neutral
  `REQ-NNN` markers, framework-agnostic.
- Worked, runnable example in `examples/test-kit-demo/` (Robot 3/3 + Playwright
  3/3 against a live API from one neutral spec).
- Original project branding: `media/logo.svg`, rebranded CLI tagline, rewritten
  governance files, README attribution to github/spec-kit (MIT).

### Notes
- See `VALIDATION.md` for acceptance-criteria evidence and known gaps.
