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
    Edit Reference  Au  testTitle1  2025
    Page Should Contain  Author and title must be at least 3 characters long

Edit With Title Too Short
    Create New Reference And Navigate To List Page
    Edit Reference  testAuthor1  Ti  2025
    Page Should Contain  Author and title must be at least 3 characters long

Edit With Year As Text
    Create New Reference And Navigate To List Page
    Edit Reference  testAuthor1  testTitle1  ysiysi
    Title Should Be  Edit reference

*** Keywords ***
Create New Reference And Navigate To List Page
    Create Reference  book  test_kw  testAuthor  testTitle  2025
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