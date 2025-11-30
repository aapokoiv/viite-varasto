*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs


*** Test Cases ***

Page Lists Reference With No Parameters
    Create Reference  article  kw1  Matti  Ensimmäinen artikkeli  2000
    Create Reference  book  kw2  Jukka  Toinen kirja  2010
    Open Reference List Page
    Page Should Contain  Ensimmäinen artikkeli
    Page Should Contain  Toinen kirja

Paging Moves Eleventh Reference to Second Page When Showing 10
    Create This Many References  11
    Open Reference List Page
    Page Should Contain  Ref 1
    Page Should Contain  Ref 10
    Page Should Not Contain  Ref 11
    Go To  ${REF_LIST_URL}?page=2&ref_amount=10
    Page Should Contain  Ref 11
    Page Should Not Contain  Ref 2

Paging Moves Twentysixth Reference When Showing 25
    Create This Many References  26
    Open Reference List Page
    Show References  25
    Page Should Contain  Ref 1
    Page Should Contain  Ref 25
    Page Should Not Contain  Ref 26
    Go To  ${REF_LIST_URL}?page=2&ref_amount=25
    Page Should Contain  Ref 26
    Page Should Not Contain  Ref 25

Paging Moves Fiftyfirst Reference When Showing 50
    Create This Many References  51
    Open Reference List Page
    Show References  50
    Page Should Contain  Ref 1
    Page Should Contain  Ref 50
    Page Should Not Contain  Ref 51
    Go To  ${REF_LIST_URL}?page=2&ref_amount=50
    Page Should Contain  Ref 51
    Page Should Not Contain  Ref 50


*** Keywords ***
Show References
    [Arguments]  ${amount}
    Wait Until Element Is Visible  id=ref_amount  10 seconds
    Select From List By Value  id=ref_amount  ${amount}

Create This Many References
    Set Selenium Speed  ${DELAY_FAST}
    [Arguments]  ${amount}
    FOR  ${i}  IN RANGE  1  ${amount}+1
        ${title}=  Evaluate  f"Ref {${i}}"
        Create Reference  article  kw${i}  Author ${i}  ${title}  2000
    END
    Set Selenium Speed  ${DELAY}