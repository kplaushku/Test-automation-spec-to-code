# Test Plan: [FEATURE NAME]

> The only neutral artifact where a framework is chosen. The spec stays
> framework-agnostic; selecting a different framework here re-targets the same
> spec without rewriting it.

## Test Groups

> Partition requirements into coherent groups; choose a framework per group.

### Group: [group-name]

- **Requirements:** REQ-001, REQ-002, ...
- **framework:** [robot | playwright]   <!-- must be allowed by the constitution -->
- **Rationale:** [why this framework fits this group and level]

### Group: [another-group]

- **Requirements:** REQ-003, ...
- **framework:** [...]
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
- **UI / mobile (future):** [MCP | source | locator-binding] - declare before
  generating any such test.
