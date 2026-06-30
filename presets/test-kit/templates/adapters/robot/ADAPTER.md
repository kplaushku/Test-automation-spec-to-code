# Adapter: Robot Framework - API + Web UI + unit

Rendering rules that turn a neutral test case (from `tasks.md`) into Robot
Framework tests. Robot is a meta-framework: it routes to a sub-library per layer
- `RequestsLibrary` (API), `SeleniumLibrary` (Web UI), `AppiumLibrary` (mobile),
and plain Python keyword libraries (unit/integration). The API rendering is
below; the UI and unit sections follow.

> For API groups, when the plan declares a `contract_source` (OpenAPI doc or
> route code), `implement` reads it to build the real endpoints/status/fields;
> otherwise the contract comes from the spec's prose.

## Capabilities

| Web UI | Mobile | API | Unit/integration | Language |
|--------|--------|-----|------------------|----------|
| **SeleniumLibrary** | via AppiumLibrary | **RequestsLibrary** | **Python keywords** | keyword-driven / Python |

## File layout

```
tests/
  <group>.robot          # one suite per group
  resources/
    keywords.robot       # shared keywords (test logic helpers)
    <group>_keywords.robot
  data/
    <group>.yaml         # named test data sets - no inline literals
  config/
    environment.yaml     # base URL, headers, auth - no inline literals
```

## Requirement marker (neutral id → native)

The `REQ-NNN` id is written as a **Robot tag** on each test case:

```robotframework
[Tags]    REQ-001
```

This is what the traceability command greps for. One test may carry several
`REQ-*` tags.

## Separation rules

- **Logic** in `*.robot` test cases and `resources/*.robot` keywords.
- **Data** in `data/*.yaml`, loaded via a variables file or `YAML` library.
  Never inline a payload or expected body in a test.
- **Config/locators** (base URL, endpoints, headers) in `config/environment.yaml`.

## Rendering a neutral case

For a task `T001 [REQ-001] orders - create order returns 201`:

```robotframework
*** Settings ***
Library           RequestsLibrary
Library           Collections
Variables         ${CURDIR}/config/environment.yaml
Variables         ${CURDIR}/data/orders.yaml
Suite Setup       Create Session    api    ${BASE_URL}    headers=${HEADERS}

*** Test Cases ***
Create Order Returns 201
    [Tags]    REQ-001
    [Documentation]    Given a valid catalog, when a valid order is posted, then 201 + order id.
    ${resp}=    POST On Session    api    /orders    json=${VALID_ORDER}
    Status Should Be    201    ${resp}
    Dictionary Should Contain Key    ${resp.json()}    id

Create Order Rejects Missing Field
    [Tags]    REQ-001
    [Documentation]    Error case: missing required field returns 422.
    ${resp}=    POST On Session    api    /orders    json=${INVALID_ORDER}    expected_status=422
    Status Should Be    422    ${resp}
```

- `${BASE_URL}`, `${HEADERS}` come from `config/environment.yaml`.
- `${VALID_ORDER}`, `${INVALID_ORDER}` come from `data/orders.yaml`.
- Precondition → `Suite Setup` / `Test Setup`; action → the request keyword;
  expected output → `Status Should Be` + body assertions.

## Run

```
pip install robotframework robotframework-requests pyyaml
robot tests/
```

`pyyaml` is required because data/config are loaded from `*.yaml` variable
files. If the target uses self-signed or otherwise unverified TLS, pass
`verify=${False}` (or a CA bundle path) to `Create Session` explicitly rather
than silencing the warning - `RequestsLibrary` does not verify by default.

## Web UI layer (SeleniumLibrary)

For UI groups, use `SeleniumLibrary`. Keep locators in a resource/variables file
(bound, never inline) and use Robot's built-in waits.

```robotframework
*** Settings ***
Library      SeleniumLibrary
Variables    ${CURDIR}/../config/locators.yaml
Variables    ${CURDIR}/../config/environment.yaml
Variables    ${CURDIR}/../data/login.yaml

*** Test Cases ***
Successful Login Shows Dashboard
    [Tags]    REQ-010
    Open Browser    ${BASE_URL}/login    headlesschrome
    Input Text       ${EMAIL_FIELD}        ${VALID_USER}[email]
    Input Password    ${PASSWORD_FIELD}     ${VALID_USER}[password]
    Click Button      xpath=//button[normalize-space()='Log in']
    Wait Until Element Is Visible    ${DASHBOARD_GREETING}    timeout=10s
    [Teardown]    Close Browser
```

- **Semantic locators** (text/role) preferred; **structural** ones come from
  `config/locators.yaml`, written inline by `implement` when the plan gives a URL
  (live DOM) or left as `__BIND__:<name>` for `speckit.qa.bind-locators`.
- **Waits:** `Wait Until ...` keywords, never `Sleep` (flaky per the constitution).
- Run: `pip install robotframework-seleniumlibrary` then `robot tests/`.

## Unit / integration layer (Python keywords)

For unit/integration, no app access is needed. Wrap the unit under test in a
Python keyword library and assert with Robot keywords.

```robotframework
*** Settings ***
Library    pricing_keywords.py    # thin wrapper over the code under test

*** Test Cases ***
Discount Applies To Eligible Cart
    [Tags]    REQ-020
    ${total}=    Apply Discount    cart=${ELIGIBLE_CART}    code=SAVE10
    Should Be Equal As Numbers    ${total}    90.00
```

Keep the keyword library (`*.py`) as the only place that imports the code under
test; the `.robot` file stays declarative. The wrapper's imports and the real
function signatures come from analyzing the plan's `source_under_test`, not from
guessing. Run: `robot tests/`.
