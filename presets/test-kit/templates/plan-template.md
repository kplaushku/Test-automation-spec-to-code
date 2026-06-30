# Test Plan: [FEATURE NAME]

> The only neutral artifact where a framework is chosen. The spec stays
> framework-agnostic; selecting a different framework here re-targets the same
> spec without rewriting it.

## Test Groups

> Partition requirements into coherent groups; choose a framework per group.

### Group: [group-name]

- **Requirements:** REQ-001, REQ-002, ...
- **framework:** [robot | playwright]   <!-- must be allowed by the constitution -->
- **level:** [api | unit | ui | mobile]
- **source_under_test:** [unit/integration only - module/package/file paths the
  tests exercise; implement reads these to generate against the real code API]
- **contract_source:** [api only, optional - OpenAPI doc (file/URL) or route
  source code; implement reads it to build the real contract]
- **Rationale:** [why this framework fits this group and level]

### Group: [another-group]

- **Requirements:** REQ-003, ...
- **framework:** [...]
- **level:** [...]
- **Rationale:** [...]

## Suite Structure

```
tests/
  <group>/            # one directory or file per group
  data/               # named test data sets (no inline literals)
  config/             # base URLs, endpoints, headers, env
```

## Fixtures, Mocks, Setup/Teardown

- **Shared:** [...]
- **Per-test:** [...]
- **Mocks/stubs:** [...]

## Test Data

> Named data sets only. Values live in `data/`, referenced by name from tests.

| Name | Purpose | Location |
|------|---------|----------|
| valid_order | happy-path payload | data/orders.* |

## Locators / Structural Identifiers

> API layer: base URLs, endpoints, headers - in `config/`, never inline.
> (UI/mobile, future: semantic locators in tests, structural ones in a locator file.)

## App-Access Strategy

- **API / contract:** none required - work from the contract.
- **UI / web:** generated only if a group is explicitly marked UI above.
  - **URL:** `[http://localhost:3000 | https://... ]` - giving a reachable URL
    lets `implement` do the **integrated single-pass** flow: navigate, read the
    DOM, and write correct locators inline (semantic preferred; structural from
    `data-testid` > role+name > id > minimal CSS).
  - **No URL at plan time:** `implement` leaves `__BIND__:<name>` placeholders;
    the **qa** extension's `speckit.qa.bind-locators` resolves them later
    (fallback), or use **source** if the frontend source is available.
