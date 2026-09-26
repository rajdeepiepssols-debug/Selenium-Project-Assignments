*** Settings ***
Library    SeleniumLibrary
Library    RequestsLibrary
Library    CustomLibrary

Suite Setup       Open Browser And Login
Suite Teardown    Close All Browsers
Test Setup        Log    Starting test case
Test Teardown     Log    Test case completed

*** Variables ***
${URL}            https://www.saucedemo.com/
${USERNAME}       standard_user
${PASSWORD}       secret_sauce
${BROWSER}        Chrome

*** Test Cases ***
Open Browser And Navigate
    [Tags]    browser    smoke
    Go To    ${URL}
    Page Should Contain Element    id=user-name

Fill Login Form
    [Tags]    login    smoke
    Go To    ${URL}
    Input Text    id=user-name    ${USERNAME}
    Input Text    name=password    ${PASSWORD}
    Page Should Contain Element    xpath=//input[@type="submit"]

Verify Login
    [Tags]    login    regression
    Page Should Contain Element    id=inventory_container

Variable Example
    [Tags]    variables
    ${full_name}=    Set Variable    ${USERNAME}
    Should Be Equal As Strings    ${full_name}    standard_user

Custom Python Keyword
    [Tags]    custom
    ${result}=    Calculate Sum    10    20
    Should Be Equal As Integers    ${result}    30

BuiltIn String Operation
    [Tags]    builtin
    ${text}=    Set Variable    Selenium Robot Framework
    ${upper}=    Convert To Upper Case    ${text}
    Should Be Equal As Strings    ${upper}    SELENIUM ROBOT FRAMEWORK

BuiltIn Mathematical Operation
    [Tags]    builtin
    ${result}=    Evaluate    10 + 20
    Should Be Equal As Integers    ${result}    30

API Response Verification
    [Tags]    api    regression
    Create Session    api    https://jsonplaceholder.typicode.com
    ${response}=    GET On Session    api    /todos/1
    ${status}=    Convert To String    ${response.status_code}
    Should Be Equal As Strings    ${status}    200

Page Assertion
    [Tags]    assertion    regression
    Page Should Contain Element    id=inventory_container

*** Keywords ***
Open Browser And Login
    Open Browser    ${URL}    ${BROWSER}
    Input Text    id=user-name    ${USERNAME}
    Input Text    name=password    ${PASSWORD}
    Click Element    xpath=//input[@type="submit"]
    Wait Until Page Contains Element    id=inventory_container