# Adapter: Selenium - Web UI

Rendering rules that turn a neutral test case (from `tasks.md`) into Selenium
WebDriver tests for the **Web UI** level. Default language: **Python** (run under
`pytest`), to share one runtime with the Robot and Playwright adapters.

## Capabilities

| Web UI | Mobile | API | Unit/integration | Language |
|--------|--------|-----|------------------|----------|
| yes | no (see Appium) | no | no | cross-language (Python recommended) |

Selenium has no API layer - API groups must use Robot or Playwright. Mobile is
its Appium counterpart (same WebDriver protocol).

## File layout (Python)

```
tests/
  test_<group>.py          # one module per group
  conftest.py              # driver fixture, base URL
  pages/<group>.py         # Page Object: methods = actions, no inline selectors
  data/<group>.json        # named test data - no inline literals
  config/locators.json     # structural locators (bound)
```

## Requirement marker (neutral id -> native)

A pytest marker plus a structured comment:

```python
@pytest.mark.req("REQ-010")
def test_successful_login(driver):  # REQ: REQ-010
    ...
```

## Separation rules

- **Logic** in test methods and Page Objects (`pages/*.py`).
- **Data** in `data/*.json`. **Structural locators** in `config/locators.json`,
  referenced by Page Objects - never inline `By.CSS_SELECTOR("...")` in a test.
- **Waits:** always `WebDriverWait` + expected conditions; never `time.sleep`
  (flaky per the constitution).

## Locator strategy (semantic preferred, structural from the live DOM)

- **Semantic** - prefer `By.XPATH` on visible text or accessible name, or a
  role-equivalent, derived from the spec.
- **Structural** - integrated when the plan gives a URL (`implement` reads the
  DOM and writes the locator inline; prefer `data-testid` > stable id > minimal
  CSS). Otherwise a `__BIND__:<name>` placeholder in `config/locators.json`,
  resolved by `speckit.qa.bind-locators`.

## Rendering a neutral UI case

```python
# conftest.py
import json, pytest
from pathlib import Path
from selenium import webdriver

@pytest.fixture
def driver():
    d = webdriver.Chrome()
    yield d
    d.quit()

@pytest.fixture(scope="session")
def L():
    return json.loads(Path("tests/config/locators.json").read_text())

@pytest.fixture(scope="session")
def base_url():
    return os.environ.get("BASE_URL", "http://localhost:3000")

@pytest.fixture(scope="session")
def creds():
    return json.loads(Path("tests/data/login.json").read_text())
```

(`import os` at the top; `creds` and `base_url` come from data/config, never inline.)

```python
# test_login.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.req("REQ-010")
def test_successful_login(driver, L, creds, base_url):  # REQ: REQ-010
    driver.get(f"{base_url}/login")
    driver.find_element(By.CSS_SELECTOR, L["email"]).send_keys(creds["valid"]["email"])
    driver.find_element(By.CSS_SELECTOR, L["password"]).send_keys(creds["valid"]["password"])
    driver.find_element(By.XPATH, "//button[normalize-space()='Log in']").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, L["dashboard_greeting"]))
    )
```

## Run

```
pip install selenium pytest
pytest tests/
```
