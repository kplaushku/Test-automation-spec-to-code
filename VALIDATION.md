# Validation status

Evidence collected against the project spec's acceptance criteria (section 13).

## Acceptance criteria

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Hand-written requirements → executable suite in the chosen framework | ✅ | `examples/test-kit-demo` runs green (Robot 3/3, Playwright 3/3) against the live JSONPlaceholder API |
| 2 | Same requirements → different frameworks by changing only the plan | ✅ | One `spec.md` + `tasks.md`; `plan.robot.md` vs `plan.playwright.md` differ only in the `framework:` line; both suites pass |
| 3 | Every test carries the requirement id it verifies | ✅ | `REQ-001..003` present as Robot `[Tags]` and Playwright `@pytest.mark.req` + `# REQ:` comment |
| 4 | Traceability command → requirement-to-test matrix, flags uncovered | ✅ (mechanism proven) | `examples/test-kit-demo/traceability.md`; neutral `REQ-NNN` extraction works across both native marker forms |
| 5 | Test data and locators separated from logic | ✅ | `robot/{config,data}` and `playwright/{config,data}` hold base URL/headers/payloads; no inline literals in tests |
| 6 | MIT attribution correct, own name + logo, governance replaced | ✅ | `LICENSE` retains GitHub copyright + adds new; README attribution; original `media/logo.svg`; governance files rewritten; CLI tagline rebranded |

## Toolkit integrity

- Repo's own structural test suite passes on the additions:
  `tests/test_presets.py tests/test_extensions.py tests/test_extension_registration.py tests/test_commands_package.py`
  → **669 passed** (648 in the version+preset+extension subset after the CLI
  rebrand, including the updated `test_cli_version` assertion).
- `specify` CLI installs and runs under Python 3.13.
- **Full suite:** `4520 passed, 73 skipped, 4 failed` → after restoring an
  over-deleted issue template (`agent_request.yml`), **3 failed**. The remaining
  3 are pre-existing upstream failures in `scripts/bash/create-new-feature.sh`
  short-word branch-naming (`"go AI now"` → `001-now` vs expected `001-ai-now`),
  in files this fork has not modified. None are caused by Specto changes.
- **End-to-end CLI install verified.** In a throwaway project:
  `specify init demo-project --integration claude --preset test-kit` installs the
  preset (`preset list` → "Test Kit v0.1.0 - enabled"); the delivered
  `speckit-specify` skill carries the test-generation content ("neutral test
  specification", `REQ-NNN`, precondition→input→object→output); and
  `preset resolve spec-template` resolves to the test-kit layer.
  `specify extension add traceability` installs the extension and registers
  `speckit.traceability.matrix`.

## Known gaps / caveats

- **CLI catalog search is remote.** `specify preset search/info` queries the
  configured remote catalog URLs, not the local bundled `presets/catalog.json`.
  `test-kit` therefore won't appear in `preset search` until this repo is
  published at the `catalog_url` (currently the placeholder
  `kplaushku/Test-automation-spec-to-code`). Install **by id** works offline from the bundled
  preset (verified above); only remote *discovery/search* is pending real
  hosting.
- **Name + repo resolved**: project named **Specto**; published to
  `github.com/kplaushku/Test-automation-spec-to-code`. The only remaining
  `your-org` strings are intentional generic examples inside the upstream
  preset/extension *authoring guides* (`presets/PUBLISHING.md`,
  `extensions/EXTENSION-*.md`), not project placeholders.
- **Robot TLS**: `RequestsLibrary` does not verify TLS by default (warning in
  the demo run); the adapter notes passing `verify` explicitly for real targets.
- **Upstream docs residue**: headlines and governance are rebranded to Specto;
  some deeper `docs/` body prose still describes the upstream software-dev
  workflow and would benefit from a test-oriented rewrite. Not blocking the
  acceptance criteria.

## Reproduce

See `examples/test-kit-demo/README.md`.
