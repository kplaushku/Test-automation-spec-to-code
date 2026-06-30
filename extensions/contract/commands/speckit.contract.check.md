---
description: Detect API contract drift - compare the live API against the spec's expectations and flag changes.
---

## User Input

```text
$ARGUMENTS  (optional: a group / REQ-NNN / endpoint to scope the check)
```

## Outline

A green API suite does not mean the API is unchanged - tests can pass while the
contract silently shifts (a field renamed, a status changed, a new required
field). This command compares **reality against expectation** and surfaces drift
before it reaches production.

1. Read `.specify/feature.json` for the feature directory. Load
   `<feature_directory>/spec.md` and
   `.specify/extensions/contract/contract-config.yml` (`base_url`, `openapi`,
   `severity`, `ignore_paths`).

2. **Build the expected contract** per endpoint, from the spec's API
   requirements: method + path, expected status code(s), and the response fields
   the requirement names (with types where stated). If `openapi` is set, reconcile
   the spec's expectations with that document and use it as the richer source.

3. **Probe the live API.** For each in-scope endpoint, send the request the spec
   describes (using the same config/data the tests use - never invent
   credentials) and capture the real status and response shape. Prefer a read-only
   or idempotent call; for mutating endpoints, use the test data fixtures.

4. **Diff expected vs actual** and classify each difference using the configured
   severity:
   - **changed_status** - the endpoint returns a different status than expected.
   - **removed_field** - a field the spec/tests rely on is gone.
   - **changed_type** - a field's type changed (e.g. `id` string -> number).
   - **new_required_field** - a new required *request* field appeared.
   - **added_field** - a new *response* field (usually safe).

5. **Report** a drift table per endpoint: requirement id, what drifted, severity,
   and the impact ("REQ-003's assertion on `total` will break"). Compute a
   **drift rate** (endpoints with fail-severity drift / total) for
   `speckit.reliability.score`. Map each drift back to the affected `REQ-NNN` and,
   when the spec is now wrong, suggest running `clarify` to re-baseline.

6. Read-only against the codebase: do not edit specs or tests. Write the drift
   report (e.g. `<feature_directory>/contract-drift.md`).
