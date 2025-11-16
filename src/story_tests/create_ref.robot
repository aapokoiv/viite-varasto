*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs

*** Test Cases ***

Create Article Reference Successfully
    Create Reference  article  Miquel  Artikkelin testaus   2020
    No Error Messages

Create Book Reference Successfully
    Create Reference  book  Matti Meikäläinen  Kirjan testaus  2018 
    No Error Messages

Create Inproceedings Reference Successfully
    Create Reference  inproceedings  Maija Mehiläinen  Konferenssijulkaisun testaus  2019
    No Error Messages

Create Misc Reference Successfully
    Create Reference  misc  Jukka Poika  Todella kaunis runo  1800
    No Error Messages

Create Reference With Too Short Author
    Create Reference  book  Kia  Testikirja  2020
    Page Should Contain  Author and title must be at least 5 characters long

Create Reference With Too Short Title
    Create Reference  article  Pekka  Jouu  2021
    Page Should Contain  Author and title must be at least 5 characters long

Create Reference With Too Long Author
    ${LONG}=    Evaluate    'a' * 301
    Create Reference  article  ${LONG}  Testi  2020
    Page Should Contain  Author and title must be at most 300 characters long

Create Reference With Too Long Title
    ${LONG}=    Evaluate    'a' * 301
    Create Reference  book  Pekka  ${LONG}  2019
    Page Should Contain  Author and title must be at most 300 characters long

Create Reference With Non-integer Year
    Create Reference  misc  Maija  Testi  year2020
    Page Should Contain  Year must be an integer

Create Reference With Year Too Small
    Create Reference  inproceedings  Matti  Testi  0
    Page Should Contain  Invalid year

Create Reference With Year Too Large
    Create Reference  article  Jukka  Testi  2027
    Page Should Contain  Invalid year



*** Keywords ***

Fill Reference Form
    [Arguments]  ${type}  ${author}  ${title}  ${year}
    Select From List By Value  name=ref_type  ${type}
    Input Text  name=ref_author  ${author}
    Input Text  name=ref_title  ${title}
    Input Text  name=ref_year  ${year}

Submit Reference
    Click Button  name=ref_submit

Create Reference
    [Arguments]  ${type}  ${author}  ${title}  ${year}
    Open New Reference Page
    Fill Reference Form  ${type}  ${author}  ${title}  ${year}
    Submit Reference

No Error Messages
    Page Should Not Contain  Author and title must be at least 5 characters long
    Page Should Not Contain  Author and title must be at most 300 characters long
    Page Should Not Contain  Invalid reference type
    Page Should Not Contain  Year must be an integer
    Page Should Not Contain  Invalid year
