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

Pageing Moves Eleventh Reference to Second Page
    FOR  ${i}  IN RANGE  1  12
        ${title}=  Evaluate  f"Ref {${i}}"
        Create Reference  article  kw${i}  Author ${i}  ${title}  2000
    END
    Open Reference List Page
    Page Should Contain  Ref 1
    Page Should Contain  Ref 10
    Page Should Not Contain  Ref 11
    Go To  ${REF_LIST_URL}?page=2
    Page Should Contain  Ref 11
    Page Should Not Contain  Ref 2