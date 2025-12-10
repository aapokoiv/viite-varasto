# User can view a list of saved references
# The list displays at least the following information for each reference: Keyword, Author, Title, Year, Type
# There are delete, edit and info buttons for each reference
# The list is shown in a clear and readable format
# If there are no saved references, the user sees a message indicating that the list is empty
# User can choose if they want 10, 20 or 50 references shown per page
# User can see 10  references per page on the viewing page
# User can see 20 references per page on the viewing page
# User can see 50 references per page on the viewing page


*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs


*** Test Cases ***

Page Lists Reference With No Parameters
    Create Reference  article  kw1  Matti  Ensimmäinen artikkeli  2000  doi=10.7000/lr1  category=ListArt
    Create Reference  book  kw2  Jukka  Toinen kirja  2010  doi=10.7000/lr2  category=ListBook
    Open Reference List Page
    Page Should Contain  Ensimmäinen artikkeli
    Page Should Contain  Toinen kirja

Paging Moves Eleventh Reference to Second Page When Showing 10
    Create This Many References Quickly  11
    Open Reference List Page
    Page Should Contain  Ref 1
    Page Should Contain  Ref 10
    Page Should Not Contain  Ref 11
    Go To  ${REF_LIST_URL}?page=2&ref_amount=10${FILTERS_URL}
    Page Should Contain  Ref 11
    Page Should Not Contain  Ref 2

Paging Moves Twentysixth Reference When Showing 25
    Create This Many References Quickly  26
    Open Reference List Page
    Show References  25
    Page Should Contain  Ref 1
    Page Should Contain  Ref 25
    Page Should Not Contain  Ref 26
    Go To  ${REF_LIST_URL}?page=2&ref_amount=25${FILTERS_URL}
    Page Should Contain  Ref 26
    Page Should Not Contain  Ref 25

Paging Moves Fiftyfirst Reference When Showing 50
    Create This Many References Quickly  51
    Open Reference List Page
    Show References  50
    Page Should Contain  Ref 1
    Page Should Contain  Ref 50
    Page Should Not Contain  Ref 51
    Go To  ${REF_LIST_URL}?page=2&ref_amount=50${FILTERS_URL}
    Page Should Contain  Ref 51
    Page Should Not Contain  Ref 50

Paging Shows First And Last Pages When In Specific Range
    Create This Many References Quickly  70
    Open Reference List Page
    Show References  10
    Page Should Contain  Next
    Page Should Not Contain Element  first-page
    Page Should Contain Element  last-page
    Go To  ${REF_LIST_URL}?page=4&ref_amount=10${FILTERS_URL}
    Page Should Contain Element  first-page
    Page Should Contain Element  last-page
    Go To  ${REF_LIST_URL}?page=7&ref_amount=10${FILTERS_URL}
    Page Should Not Contain Element  last-page
    Page Should Contain Element  first-page

Paging Shows Two Pages Forward And Back From Currently Selected
    Create This Many References Quickly  50
    Go To  ${REF_LIST_URL}?page=3&ref_amount=10${FILTERS_URL}
    Page Should Contain Element  page-1
    Page Should Contain Element  page-2
    Page Should Contain Element  page-4
    Page Should Contain Element  page-5


*** Keywords ***
Show References
    [Arguments]  ${amount}
    Wait Until Page Contains Element  class=refs-table  60 seconds
    Wait Until Element Is Visible  id=ref_amount  60 seconds
    Select From List By Value  id=ref_amount  ${amount}
