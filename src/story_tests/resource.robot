*** Settings ***
Library  SeleniumLibrary
Library  ../repositories/citation_repository.py

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      0.5 seconds
${DELAY_FAST}      0.01 seconds
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${NEW_REF_URL}  http://${SERVER}/new_ref
${REF_LIST_URL}  http://${SERVER}/view_refs
${FILTERS_URL}  &query=&type=-&category=-&year_from=0&year_to=2025
${REF_SELECT_URL}  http://${SERVER}/select_refs
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
        Set Selenium Speed  0.1 seconds
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Reset Todos
    Go To  ${RESET_URL}

Reset Refs
    Wait Until Keyword Succeeds  30  1  Go To  ${RESET_URL}
    Wait Until Keyword Succeeds  30  1  Go To  ${HOME_URL}

Open Home Page
    Go To  ${HOME_URL}

Open New Reference Page
    Go To  ${NEW_REF_URL}

Open Reference List Page Raw
    Go To  ${REF_LIST_URL}

Open Reference List Page
    Go To  ${REF_LIST_URL}
    Wait Until Page Contains Element  class=refs-table  30 seconds

Fill Reference Form
    [Arguments]  ${type}  ${keyword}  ${author}  ${title}  ${year}  ${doi}=None  ${category}=None  ${journal}=None  ${volume}=None  ${pages}=None  ${publisher}=None  ${booktitle}=None
    Go To    ${NEW_REF_URL}
    Select From List By Value    id=ref_type    ${type}
    Input Text  name=ref_keyword  ${keyword}
    Input Text  name=ref_author  ${author}
    Input Text  name=ref_title  ${title}
    Input Text  name=ref_year  ${year}

    Input Text If Visible  name=ref_doi  ${doi}
    Input Text If Visible  name=ref_category  ${category}
    Input Text If Visible  name=ref_journal  ${journal}
    Input Text If Visible  name=ref_volume  ${volume}
    Input Text If Visible  name=ref_pages  ${pages}
    Input Text If Visible  name=ref_publisher  ${publisher}
    Input Text If Visible  name=ref_booktitle  ${booktitle}

Fill ACM Form
    [Arguments]  ${acm-url}  ${keyword}  ${category}=None
    Go To    ${NEW_REF_URL}
    Input Text  name=ref_acm_url  ${acm-url}
    Input Text If Visible  name=ref_keyword_acm  ${keyword}
    Input Text If Visible  name=ref_category_acm  ${category}

Input Text If Visible
    [Arguments]  ${locator}  ${value}
    Run Keyword If  '${value}' == 'None'  Return From Keyword
    ${visible}=  Run Keyword And Return Status  Element Should Be Visible  ${locator}
    Run Keyword If  ${visible}  Input Text  ${locator}  ${value}


Submit Reference
    Click Button  name=ref_submit

Create Reference
    [Arguments]  ${type}  ${keyword}  ${author}  ${title}  ${year}  ${doi}=None  ${category}=None  ${journal}=None  ${volume}=None  ${pages}=None  ${publisher}=None  ${booktitle}=None
    Open New Reference Page
    Fill Reference Form  ${type}  ${keyword}   ${author}  ${title}  ${year}  ${doi}  ${category}  ${journal}  ${volume}  ${pages}  ${publisher}  ${booktitle}
    Submit Reference

Create Reference From ACM
    [Arguments]  ${acm-url}  ${keyword}=None  ${category}=None
    Open New Reference Page
    Fill ACM Form  ${acm-url}  ${keyword}  ${category}
    Click Button  name=acm_submit

Create This Many References Quickly
    [Arguments]  ${amount}
    Create Test Refs Quickly  ${amount}

Filter References By Selection
    [Arguments]  ${filter}  ${value}
    Select From List By Value  ${filter}  ${value}
    Click Button  Filter

Filter References By Search
    [Arguments]  ${value}
    Input Text  query  ${value}
    Click Button  Filter

Filter References By Category
    [Arguments]  ${category}
    Select From List By Value  id=category  ${category}
    Click Button  Filter

Filter References by Year
    [Arguments]  ${minYearID}  ${minYear}  ${maxYearID}  ${maxYear}
    Input Text  id:${minYearID}  ${minYear}
    Input Text  id:${maxYearID}  ${maxYear}
    Click Button  Filter

No Error Messages
    Page Should Not Contain  Author and title must be at least 5 characters long
    Page Should Not Contain  Author and title must be at most 300 characters long
    Page Should Not Contain  Invalid reference type
    Page Should Not Contain  Year must be an integer
    Page Should Not Contain  Invalid year
    Page Should Not Contain  Volume must be an integer
    Page Should Not Contain  Pages must be at most 300 characters long
    Page Should Not Contain  Journal must be at most 300 characters long
    Page Should Not Contain  Publisher must be at most 300 characters long
    Page Should Not Contain  Booktitle must be at most 300 characters long

