# Suite Reliability extension

Turns trust into a metric. Test automation fails its users when the suite is not
*believed* - flaky reds get ignored, green is assumed safe. This extension makes
reliability measurable and enforceable.

## Commands

| Command | What it does |
|---|---|
| `speckit.reliability.flake` | Runs each test `flake_runs` times, computes a flake score, and **quarantines** (tags) tests that fall in the flaky band - enforcing the constitution's flaky definition. |
| `speckit.reliability.score` | Rolls four signals into one 0-100 **trust score**: requirement coverage, flake-free rate, assertion strength, and drift-free rate. Reports PASS/FAIL vs `min_score` and the top actions to improve. |

## The score

```
reliability =  0.35 * requirement_coverage   (traceability ext)
             + 0.30 * flake_free             (reliability.flake)
             + 0.20 * assertion_strength     (qa.verify)
             + 0.15 * drift_free             (contract.check, qa.heal)
```

Weights and `min_score` are configurable in `reliability-config.yml`. Missing
signals are surfaced (not assumed) so the score never lies by omission.

## How it fits

It is a **meta layer** over the other extensions - it consumes their reports
rather than re-doing their work:

- coverage from [`traceability`](../traceability/)
- false-greens from [`qa`](../qa/) `qa.verify`
- drift from [`contract`](../contract/) and `qa.heal`

Quarantined tests keep the main signal clean; a CI recipe can run them apart and
track whether they are getting fixed or accumulating.
