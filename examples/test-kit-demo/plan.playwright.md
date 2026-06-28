# Test Plan: Posts API (demo) — Playwright variant

> Identical to the Robot variant except for the `framework:` line. This is the
> whole point: re-targeting the same spec is a one-line change.

## Test Groups

### Group: posts

- **Requirements:** REQ-001, REQ-002, REQ-003
- **framework:** playwright
- **Rationale:** API/contract level; Playwright `request` (Python) is in scope.

## Suite Structure

```
playwright/
  tests/test_posts.py
  conftest.py
  pytest.ini
  config/environment.json   # base URL, headers
  data/posts.json           # named payloads
```

## Test Data

| Name | Purpose | Location |
|------|---------|----------|
| valid_post | create-post payload | data/posts.json |

## Locators / Structural Identifiers

Base URL and headers in `config/environment.json`. No inline literals.

## App-Access Strategy

None — API/contract works from the contract.
