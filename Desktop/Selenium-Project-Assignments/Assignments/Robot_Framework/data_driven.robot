*** Settings ***
Library    SeleniumLibrary
Library    DataDriver    file=test_data.csv
Test Template    Login With Different Data
Suite Setup    Open Browser
Suite Teardown    Close All Browsers

*** Variables ***
${URL}    https://www.saucedemo.com/

*** Test Cases ***
Login Test

*** Keywords ***
Login With Different Data
    [Arguments]    ${username}    ${password}    ${expected}
    Go To    ${URL}
    Input Text    id=user-name    ${username}
    Input Text    name=password    ${password}
    Click Element    xpath=//input[@type="submit"]

    IF    '${expected}' == 'success'
        Page Should Contain Element    id=inventory_container
    ELSE
        Page Should Contain Element    css=h3[data-test="error"]
    END