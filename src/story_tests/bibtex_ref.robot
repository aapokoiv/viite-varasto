*** Settings ***
Resource  resource.robot
Library  RequestsLibrary
Library  Collections
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs

*** Test Cases ***
Export Button Hidden When No references
    Go To  ${REF_LIST_URL}
    Wait Until Page Contains  View all the references  10 seconds
    Page Should Not Contain Button  Lataa BibTeX

Export Button And Alert Present On Reference List Page
    Create Reference  article  bibtex-kw  BibTeX Author  BibTeX  2021  journal=Journal  volume=5  pages=100-110
    Open Reference List Page
    Click Button  Lataa BibTeX
    Alert Should Be Present

Create BibTeX Reference Successfully
    Create Reference  article  bibtex-kw  BibTeX Author  BibTeX  2021  journal=Journal  volume=5  pages=100-110
    Open Reference List Page
    # tee HTTP-pyyntö suoraan palvelimelle (ei selaimen latausta)
    Create Session    api    ${HOME_URL}
    ${resp}=    GET On Session    api    /export_bibtex
    Should Be Equal As Integers    ${resp.status_code}    200
    ${cd}=    Get From Dictionary    ${resp.headers}    Content-Disposition
    Should Contain    ${cd}    attachment
    Should Contain    ${resp.text}    author = {BibTeX Author},
    Should Contain    ${resp.text}    title = {BibTeX},
    Should Contain    ${resp.text}    year = {2021},
    Should Contain    ${resp.text}    journal = {Journal}
    Should Contain    ${resp.text}    volume = {5},
    Should Contain    ${resp.text}    pages = {100-110}
