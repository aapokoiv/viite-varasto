*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      0.5 seconds
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${NEW_REF_URL}  http://${SERVER}/new_ref
${REF_LIST_URL}  http://${SERVER}/view_refs
${BROWSER}    chrome
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    IF  $BROWSER == 'chrome'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
        Call Method  ${options}  add_argument  --incognito
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
        Call Method  ${options}  add_argument  --private-window
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0.01 seconds
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Reset Todos
    Go To  ${RESET_URL}

Reset Refs
    Go To  ${RESET_URL}
    Go To  ${HOME_URL}

Open Home Page
    Go To  ${HOME_URL}

Open New Reference Page
    Go To  ${NEW_REF_URL}

Open Reference List Page
    Go To  ${REF_LIST_URL}

Fill Reference Form
    [Arguments]  ${type}  ${keyword}  ${author}  ${title}  ${year}
    Select From List By Value  name=ref_type  ${type}
    Input Text  name=ref_keyword  ${keyword}
    Input Text  name=ref_author  ${author}
    Input Text  name=ref_title  ${title}
    Input Text  name=ref_year  ${year}

Submit Reference
    Click Button  name=ref_submit

Create Reference
    [Arguments]  ${type}  ${keyword}  ${author}  ${title}  ${year}
    Open New Reference Page
    Fill Reference Form  ${type}  ${keyword}  ${author}  ${title}  ${year}
    Submit Reference

Filter References By Selection
    [Arguments]  ${filter}  ${value}
    Select From List By Value  ${filter}  ${value}
    Click Button  Filter

Filter References By Search
    [Arguments]  ${value}
    Input Text  query  ${value}
    Click Button  Filter

No Error Messages
    Page Should Not Contain  Author and title must be at least 5 characters long
    Page Should Not Contain  Author and title must be at most 300 characters long
    Page Should Not Contain  Invalid reference type
    Page Should Not Contain  Year must be an integer
    Page Should Not Contain  Invalid year
