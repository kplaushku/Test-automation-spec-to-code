# Adapter: Robot Framework — API layer

Rendering rules that turn a neutral test case (from `tasks.md`) into Robot
Framework tests for the **API / contract** level, using `RequestsLibrary`.

## Capabilities

| Web UI | Mobile | API | Unit/integration | Language |
|--------|--------|-----|------------------|----------|
| via SeleniumLibrary | via AppiumLibrary | **RequestsLibrary** | Python keywords | keyword-driven / Python |

Robot is a meta-framework: for the API layer it routes to `RequestsLibrary`.
Only the API rendering is defined here; UI/mobile sub-adapters come later.

## File layout

```
tests/
  <group>.robot          # one suite per group
  resources/
    keywords.robot       # shared keywords (test logic helpers)
    <group>_keywords.robot
  data/
    <group>.yaml         # named test data sets — no inline literals
  config/
    environment.yaml     # base URL, headers, auth — no inline literals
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

For a task `T001 [REQ-001] orders — create order returns 201`:

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
than silencing the warning — `RequestsLibrary` does not verify by default.
