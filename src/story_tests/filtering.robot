*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs


*** Test Cases ***

Page Lists References Filtered By Type
    Create Reference  article  kw1  Matti  Ensimmäinen artikkeli  2000
    Create Reference  book  kw2  Jukka  Toinen kirja  2010
    Open Reference List Page
    Filter References By Selection  type  book
    Page Should Contain  Jukka
    Page Should Not Contain  Matti

Page Lists References Filtered By Search
    Create Reference  article  kw1  Matti  Ensimmäinen artikkeli  2000
    Create Reference  book  kw2  Jukka  Toinen kirja  2010
    Open Reference List Page
    Filter References By Search  Ensimmäinen
    Page Should Contain  Matti
    Page Should Not Contain  Jukka
