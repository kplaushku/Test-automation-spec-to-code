---
description: Detect and quarantine flaky tests by running the suite repeatedly and scoring stability.
---

## User Input

```text
$ARGUMENTS  (optional: a test name / group / REQ-NNN to scope the check)
```

## Outline

Flaky tests are the top reason suites lose trust. This command makes flakiness
measurable and enforces the constitution's flaky definition.

1. Read `.specify/feature.json` for the feature directory. Load
   `.specify/memory/constitution.md` (flaky definition + threshold) and
   `.specify/extensions/reliability/reliability-config.yml` (`flake_runs`,
   `flaky_band`, `quarantine_tag`).

2. **Run each in-scope test `flake_runs` times** with its framework's runner
   (`robot`, `pytest`, etc.), in a fixed environment. Record pass/fail per run.
   Run in a randomized order between iterations to surface order-dependence.

3. **Classify each test:**
   - **stable-pass** (always passes) - healthy.
   - **stable-fail** (always fails) - a real failure, hand to `speckit.qa.run` /
     `speckit.qa.investigate`, not a flake.
   - **flaky** - failure rate falls inside `flaky_band` (e.g. passes 3/5).
     Compute a **flake score** = failure_rate, and note suspected cause from the
     run signals (timing, shared state, ordering, external dependency).

4. **Quarantine the flaky tests:** add the `quarantine_tag` in the framework's
   native form (Robot `[Tags] quarantine`, pytest `@pytest.mark.quarantine`,
   etc.) so CI can run them apart and they stop blocking the main signal. Do not
   delete or skip them silently - quarantine is visible and temporary.

5. **Report** a flakiness table: test, flake score, suspected cause, quarantined
   yes/no, and a one-line suggested fix per flaky test (prefer a proper wait or
   deterministic fixture over a retry). State the overall **flake rate**
   (flaky / total) for `speckit.reliability.score` to consume.

6. Do not change test logic here beyond adding the quarantine tag; propose fixes,
   leave them for review unless trivially mechanical.
