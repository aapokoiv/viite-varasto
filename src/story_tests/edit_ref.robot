*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs

*** Test Cases ***  
Clicking Edit Button Redirects Correctly
    Create New Reference And Navigate To List Page
    Title Should Be  Edit reference
    
Edit With Correct Inputs
    Create New Reference And Navigate To List Page
    Edit Reference  testAuthor1  testTitle1  2024
    No Error Messages

Edit With Author Too Short
    Create New Reference And Navigate To List Page
    Edit Reference  Auth  testTitle1  2025
    Page Should Contain  Author and title must be at least 5 characters long

Edit With Author Too Long
    ${LONG}=    Evaluate    'a' * 301
    Create New Reference And Navigate To List Page
    Edit Reference  ${LONG}  testTitle1  2025
    Page Should Contain  Author and title must be at most 300 characters long

Edit With Title Too Short
    Create New Reference And Navigate To List Page
    Edit Reference  testAuthor1  Titl  2025
    Page Should Contain  Author and title must be at least 5 characters long

Edit With Title Too Long
    ${LONG}=    Evaluate    'a' * 301
    Create New Reference And Navigate To List Page
    Edit Reference  testAuthor1  ${LONG}  2025
    Page Should Contain  Author and title must be at most 300 characters long

Edit With Year Too Early
    Create New Reference And Navigate To List Page
    Edit Reference  testAuthor1  testTitle1  0
    Page Should Contain  Invalid year

Edit With Year Too Late
    Create New Reference And Navigate To List Page
    Edit Reference  testAuthor1  testTitle1  2030
    Page Should Contain  Invalid year

Edit With Year As Text
    Create New Reference And Navigate To List Page
    Edit Reference  testAuthor1  testTitle1  ysiysi
    Title Should Be  Edit reference

*** Keywords ***
Create New Reference And Navigate To List Page
    Create Reference  book  testAuthor  testTitle  2025
    Open Reference List Page
    Click Button  Muokkaa

Submit Edit
    Click Button  Edit

Fill Edit Form
    [Arguments]  ${author}  ${title}  ${year}
    Input Text  name=ref_author  ${author}
    Input Text  name=ref_title  ${title}
    Input Text  name=ref_year  ${year}

Edit Reference
    [Arguments]  ${author}  ${title}  ${year}
    Fill Edit Form  ${author}  ${title}  ${year}
    Submit Edit