# Test Plan: Posts API (demo) — Robot variant

> Identical to the Playwright variant except for the `framework:` line.

## Test Groups

### Group: posts

- **Requirements:** REQ-001, REQ-002, REQ-003
- **framework:** robot
- **Rationale:** API/contract level; Robot via RequestsLibrary is in scope and default.

## Suite Structure

```
robot/
  tests/posts.robot
  config/environment.yaml   # base URL, headers
  data/posts.yaml           # named payloads
```

## Test Data

| Name | Purpose | Location |
|------|---------|----------|
| VALID_POST | create-post payload | data/posts.yaml |

## Locators / Structural Identifiers

Base URL and headers in `config/environment.yaml`. No inline literals.

## App-Access Strategy

None — API/contract works from the contract.
