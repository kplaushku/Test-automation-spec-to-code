# Adapter: Playwright - API layer

Rendering rules that turn a neutral test case (from `tasks.md`) into Playwright
tests for the **API / contract** level, using the `request` fixture. Default
language: **Python** (`pytest-playwright`), to share one runtime with the Robot
adapter. A TypeScript variant is noted at the end.

## Capabilities

| Web UI | Mobile | API | Unit/integration | Language |
|--------|--------|-----|------------------|----------|
| yes | web emulation only | **request fixture** | partial | TS, JS, Python, .NET, Java |

## File layout (Python)

```
tests/
  test_<group>.py        # one module per group
  conftest.py            # fixtures: base URL, headers, api context
  data/
    <group>.json         # named test data sets - no inline literals
  config/
    environment.json     # base URL, headers, auth - no inline literals
```

## Requirement marker (neutral id → native)

The `REQ-NNN` id is written as a **pytest marker** AND a structured comment, so
the traceability command can grep either form:

```python
import pytest

@pytest.mark.req("REQ-001")   # registered in pytest.ini: markers = req(id): requirement id
def test_create_order_returns_201(api):  # REQ: REQ-001
    ...
```

Register the marker once in `pytest.ini`:

```ini
[pytest]
markers =
    req(id): the REQ-NNN requirement this test verifies
```

## Separation rules

- **Logic** in `test_*.py`.
- **Data** in `data/*.json`, loaded by a fixture. Never inline a payload or
  expected body.
- **Config/locators** (base URL, endpoints, headers) in `config/environment.json`,
  exposed through the `api` request-context fixture in `conftest.py`.

## Rendering a neutral case

For a task `T001 [REQ-001] orders - create order returns 201`:

```python
# conftest.py
import json, pytest
from pathlib import Path
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def env():
    return json.loads(Path("tests/config/environment.json").read_text())

@pytest.fixture
def api(env):
    with sync_playwright() as p:
        ctx = p.request.new_context(base_url=env["base_url"],
                                    extra_http_headers=env["headers"])
        yield ctx
        ctx.dispose()

@pytest.fixture(scope="session")
def orders():
    return json.loads(Path("tests/data/orders.json").read_text())
```

```python
# test_orders.py
import pytest

@pytest.mark.req("REQ-001")
def test_create_order_returns_201(api, orders):  # REQ: REQ-001
    # Given a valid catalog, when a valid order is posted, then 201 + order id.
    resp = api.post("/orders", data=orders["valid_order"])
    assert resp.status == 201
    assert "id" in resp.json()

@pytest.mark.req("REQ-001")
def test_create_order_rejects_missing_field(api, orders):  # REQ: REQ-001
    # Error case: missing required field returns 422.
    resp = api.post("/orders", data=orders["invalid_order"])
    assert resp.status == 422
```

## Run

```
pip install pytest-playwright && playwright install
pytest tests/
```

## TypeScript variant

If the project's constitution sets the Playwright language to TS, use
`@playwright/test` with `request` and `test(..., { tag: '@REQ-001' })` plus a
`// REQ: REQ-001` comment. Same separation rules; data in `data/*.json`, config
in `playwright.config.ts`.
