# API Contract Drift extension

Catches the silent failure mode: **the suite is green, but the API changed.**
Tests assert what they were written against; if the live contract drifts - a
field renamed, a status code changed, a new required field - the suite can stay
green while production breaks. This extension compares reality against the spec's
expectations and flags the drift.

## Command

| Command | What it does |
|---|---|
| `speckit.contract.check` | Builds the expected contract from the spec's API requirements (optionally reconciled with an OpenAPI doc), probes the live API, diffs expected vs actual, and reports drift mapped back to each `REQ-NNN`. |

## What it detects

| Drift | Default severity | Example |
|---|---|---|
| Changed status code | fail | `POST /orders` now returns 200 instead of 201 |
| Removed field | fail | response no longer includes `total` |
| Changed type | fail | `id` changed from string to number |
| New required request field | warn | `POST /orders` now requires `currency` |
| Added response field | warn | new `created_at` field (usually safe) |

Severity is configurable in `contract-config.yml`.

## How it fits

- Strongest on the **API/contract** layer, where Specto is most mature.
- Feeds a `drift_rate` into the [`reliability`](../reliability/) score, so contract
  health shows up in the suite's trust number.
- When drift means the **spec** is now outdated, it points you back to `clarify`
  to re-baseline rather than silently patching tests.
