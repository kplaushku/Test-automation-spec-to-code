---
description: Compute a single suite reliability score from coverage, flakiness, assertion strength, and drift.
---

## User Input

```text
$ARGUMENTS
```

## Outline

Answers the question users actually have: **"can I trust this suite?"** It rolls
the signals other commands produce into one 0-100 score, so reliability is a
number you can gate on, not a feeling.

1. Read `.specify/feature.json`; load
   `.specify/extensions/reliability/reliability-config.yml` (`score_weights`,
   `min_score`) and `.specify/memory/constitution.md`.

2. **Gather the four signals** (use the latest available; note any that are
   missing rather than assuming a value):
   - **requirement_coverage** - from `speckit.traceability.matrix`
     (covered / total requirements).
   - **flake_free** - `1 - flake_rate` from `speckit.reliability.flake`.
   - **assertion_strength** - `1 - false_green_rate` from `speckit.qa.verify`
     (weak + false-green tests / total).
   - **drift_free** - `1 - drift_rate` from `speckit.contract.check` (API) and
     selector-drift incidents from `speckit.qa.run` / `speckit.qa.heal`.

3. **Compute the score:** weighted sum of the four signals (weights from config,
   normalized if a signal is unavailable) scaled to 0-100.

4. **Report** a compact reliability card:
   - the headline score and PASS/FAIL vs `min_score`;
   - the four sub-scores with the weakest one called out;
   - the top 3 concrete actions to raise the score (e.g. "cover REQ-007",
     "quarantine and fix 2 flaky tests", "strengthen 1 weak assertion"); and
   - which signals were stale/missing and which command to run to refresh them.

5. Read-only: do not modify tests, data, or specs. Only read prior reports and
   write the reliability card (e.g. `<feature_directory>/reliability.md`).
