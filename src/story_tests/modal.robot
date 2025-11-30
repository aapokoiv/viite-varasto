*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs


*** Test Cases ***

Modal Shows Citation Details
    Create Reference  article  kw_modal  Alice  Modal Test  2022  J Test  1  10-20  Pub
    Open Reference List Page
    Click Element  css:.info-btn
    Wait Until Element Is Visible  css:.modal-content  5 seconds

    Element Text Should Be  id=m-title  Modal Test
    Element Text Should Be  id=m-author  Alice
    Element Text Should Be  id=m-year  2022
    Element Should Be Visible  id=m-journal
    Element Should Be Visible  id=m-volume
    Element Should Be Visible  id=m-pages
    Element Should Be Visible  id=m-publisher
