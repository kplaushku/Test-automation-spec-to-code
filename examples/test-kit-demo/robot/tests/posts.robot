*** Settings ***
Library           RequestsLibrary
Library           Collections
Variables         ${CURDIR}/../config/environment.yaml
Variables         ${CURDIR}/../data/posts.yaml
Suite Setup       Create Session    api    ${BASE_URL}    headers=${HEADERS}

*** Test Cases ***
Fetch Existing Post Returns 200 With Fields
    [Tags]    REQ-001
    [Documentation]    Given the API is up, when GET /posts/1, then 200 with expected fields.
    ${resp}=    GET On Session    api    /posts/1
    Status Should Be    200    ${resp}
    ${body}=    Set Variable    ${resp.json()}
    Should Be Equal As Integers    ${body}[id]    1
    Should Not Be Empty    ${body}[title]
    Should Not Be Empty    ${body}[body]

Create Post Returns 201 With Id
    [Tags]    REQ-002
    [Documentation]    Given the API is up, when POST /posts with a valid body, then 201 with a new id.
    ${resp}=    POST On Session    api    /posts    json=${VALID_POST}
    Status Should Be    201    ${resp}
    Dictionary Should Contain Key    ${resp.json()}    id
    ${id}=    Convert To Integer    ${resp.json()}[id]
    Should Be True    ${id} > 0

Fetch Missing Post Returns 404
    [Tags]    REQ-003
    [Documentation]    Given the API is up, when GET /posts/9999, then 404.
    ${resp}=    GET On Session    api    /posts/9999    expected_status=404
    Status Should Be    404    ${resp}
