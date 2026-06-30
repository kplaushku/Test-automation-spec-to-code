# Adapter: Appium - mobile native

Rendering rules that turn a neutral test case (from `tasks.md`) into Appium tests
for **native mobile** (iOS, Android) over the WebDriver protocol. Default
language: **Python** (`Appium-Python-Client`, run under `pytest`).

## Capabilities

| Web UI | Mobile | API | Unit/integration | Language |
|--------|--------|-----|------------------|----------|
| no (use Selenium/Playwright) | **iOS + Android** | no | no | cross-language (Python recommended) |

> **Execution note:** unlike API/web, a live run needs a running **Appium server**
> plus a real device or emulator/simulator. Specto generates the test and binds
> locators from the element tree; provisioning the device is the user's CI/runner
> concern.

## File layout (Python)

```
tests/
  test_<group>.py          # one module per group
  conftest.py              # appium driver fixture + desired capabilities
  screens/<group>.py       # Screen Object: actions, no inline locators
  data/<group>.json        # named test data - no inline literals
  config/
    capabilities.json      # platform, device, app path - no inline literals
    locators.json          # structural locators (bound)
```

## Requirement marker (neutral id -> native)

A pytest marker plus a structured comment:

```python
@pytest.mark.req("REQ-030")
def test_add_to_cart(driver):  # REQ: REQ-030
    ...
```

## Separation rules

- **Logic** in test methods and Screen Objects (`screens/*.py`).
- **Capabilities** (platform, deviceName, app) in `config/capabilities.json`.
- **Locators** in `config/locators.json` - prefer **accessibility id**
  (cross-platform), then platform locators (`-ios predicate string`,
  `UiAutomator`). Never inline.
- **Waits:** `WebDriverWait` + expected conditions; never `time.sleep`.

## Locator strategy (accessibility-first, structural bound)

- **Accessibility id** is the most stable and is often knowable from the spec's
  labels - prefer it.
- **Structural** locators come from the app's **element tree**. When a device is
  available at generation time, `implement`/`qa.bind-locators` reads the tree and
  writes them inline; otherwise they are `__BIND__:<name>` placeholders.

## Rendering a neutral case

```python
# conftest.py
import json, pytest
from pathlib import Path
from appium import webdriver
from appium.options.common import AppiumOptions

@pytest.fixture
def driver():
    caps = json.loads(Path("tests/config/capabilities.json").read_text())
    d = webdriver.Remote("http://localhost:4723", options=AppiumOptions().load_capabilities(caps))
    yield d
    d.quit()

@pytest.fixture(scope="session")
def L():
    return json.loads(Path("tests/config/locators.json").read_text())
```

```python
# test_cart.py
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.req("REQ-030")
def test_add_to_cart(driver, L):  # REQ: REQ-030
    driver.find_element(AppiumBy.ACCESSIBILITY_ID, "add-to-cart").click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, L["cart_badge"]))
    )
```

## Run

```
pip install Appium-Python-Client pytest
# requires an Appium server (npm i -g appium) + a device/emulator
appium &
pytest tests/
```
