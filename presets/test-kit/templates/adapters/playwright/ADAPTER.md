# Adapter: Playwright - API + UI layers

Rendering rules that turn a neutral test case (from `tasks.md`) into Playwright
tests. Two layers: **API / contract** (the `request` fixture) and **UI / web**
(the DOM-integrated `page` fixture - see the UI section below). Default
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

## UI / web layer (DOM-integrated)

For UI groups, render real browser tests using the integrated Playwright API
(the `page` fixture from `pytest-playwright`), not the `request` fixture.

### Locator strategy (semantic inline, structural from the live DOM)

Applies only when the plan chose a UI group (see `implement`'s gated UI rule).

- **Semantic locators inline** - use the Playwright role/label/text API derived
  from the spec's visible labels: `page.get_by_role("button", name="Log in")`,
  `page.get_by_label("Email")`, `page.get_by_text(...)`. These need no app
  access and are the preferred, stable form.
- **Structural locators, two modes:**
  - **Integrated (default when the plan gave a URL + a browser is available):**
    `implement` navigates to the app, reads the real DOM, and writes the correct
    structural locator **inline in one pass** (`data-testid` > role+name >
    stable `id` > minimal CSS).
  - **Fallback (no app access at generation time):** emit a `__BIND__:<name>`
    placeholder in the locator file for `speckit.qa.bind-locators` to resolve
    later. Never inline a guessed css/xpath selector.

### Rendering a neutral UI case

For a task `T010 [REQ-010] login - successful login shows dashboard`:

```python
import pytest
from playwright.sync_api import expect

from .locators import L   # bound structural locators, loaded from the locator file


@pytest.mark.req("REQ-010")
def test_successful_login_shows_dashboard(page, base_url, creds):  # REQ: REQ-010
    page.goto(f"{base_url}/login")
    # Semantic locators (real Playwright API, no binding needed):
    page.get_by_label("Email").fill(creds["valid"]["email"])
    page.get_by_label("Password").fill(creds["valid"]["password"])
    page.get_by_role("button", name="Log in").click()
    # Structural locator bound from the live DOM via qa.bind-locators:
    expect(page.locator(L["dashboard_greeting"])).to_be_visible()
```

- **Auto-wait:** rely on Playwright's built-in auto-wait and `expect(...)`
  retrying assertions. Do **not** add bare `sleep`s (flaky per the constitution).
- **Fixtures:** `page` (and `browser`/`context`) come from `pytest-playwright`;
  `base_url` and `creds` from config/data files - never inline.
- **Evidence on failure:** enable trace + screenshot so `speckit.qa.run` can
  triage UI failures (`--tracing=retain-on-failure --screenshot=only-on-failure`).

## Run

```
# API only:
pip install pytest-playwright
pytest tests/

# UI (needs browser binaries):
playwright install
pytest tests/ --tracing=retain-on-failure --screenshot=only-on-failure
```

For UI groups, resolve `__BIND__` placeholders first with
`speckit.qa.bind-locators` against the running app.

## TypeScript variant

If the project's constitution sets the Playwright language to TS, use
`@playwright/test` with `request` and `test(..., { tag: '@REQ-001' })` plus a
`// REQ: REQ-001` comment. Same separation rules; data in `data/*.json`, config
in `playwright.config.ts`.
