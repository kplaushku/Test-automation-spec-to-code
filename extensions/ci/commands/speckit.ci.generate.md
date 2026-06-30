---
description: Generate a CI workflow that runs the suite, isolates quarantined flaky tests, and publishes reliability artifacts.
---

## User Input

```text
$ARGUMENTS  (optional: github | gitlab to force the provider)
```

## Outline

Makes reliability visible on every push. Generates a CI config tailored to the
suite Specto produced - it does not invent test commands, it reads the plan.

1. Read `.specify/feature.json`; load `plan.md` (frameworks per group),
   `.specify/memory/constitution.md` (coverage/reliability thresholds), and
   `.specify/extensions/ci/ci-config.yml` (`provider`, `triggers`,
   `quarantine`, `publish`, `min_reliability_score`).

2. **Resolve the runners** from the frameworks actually used:
   - `robot` -> `pip install robotframework ...` + `robot tests/`
   - `playwright` (py) -> `pip install pytest-playwright` (+ `playwright install`
     for UI) + `pytest`
   - `cypress` -> `npm ci` + `npx cypress run`
   - `selenium` / `appium` -> their Python runners (Appium also needs a device
     job - emit it as a documented, manually-enabled job, not a silent failure).

3. **Generate the workflow** for the chosen provider (see the reference files in
   this extension's `templates/`). It must have:
   - a **main test job** that installs deps and runs each framework's suite,
     keyed to the requirement ids;
   - a **quarantine job** per `ci-config.yml` `quarantine`: when `separate`, run
     only tests tagged `quarantine` in a **non-blocking** job (`continue-on-error`
     / `allow_failure`) so flaky tests are tracked but never break the build;
   - **publish steps** that upload `traceability.md`, `reliability.md`, and
     `contract-drift.md` as artifacts / job-summary when `publish` enables them;
   - an optional **gate** that fails the build when the reliability score is
     below `min_reliability_score`.

4. **Write** the file (`.github/workflows/specto-tests.yml` or
   `.gitlab-ci.yml`). Do not overwrite an existing CI file without saying so -
   show a diff and confirm.

5. **Report** what was generated: jobs, which frameworks each runs, how
   quarantine is handled, and what is published. Note any job the user must
   finish wiring (secrets, a device farm for Appium).
