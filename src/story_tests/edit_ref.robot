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
    Edit Reference  misc  testAuthor1  testTitle1  2024
    No Error Messages

Edit Article With Correct Inputs And Optional Fields
    Create New Reference And Navigate To List Page
    Edit Reference  article  testAuthor1  testTitle1  2024  journal=journal  volume=1  pages=32-34
    No Error Messages

Edit Book With Correct Inputs And Optional Field
    Create New Reference And Navigate To List Page
    Edit Reference  book  testAuthor1  testTitle1  2024  publisher=publisher
    No Error Messages

Edit Inproceedings With Correct Inputs And Optional Field
    Create New Reference And Navigate To List Page
    Edit Reference  inproceedings  testAuthor1  testTitle1  2024  booktitle=booktitle
    No Error Messages

Edit With Author Too Short
    Create New Reference And Navigate To List Page
    Edit Reference  misc  Auth  testTitle1  2025
    Page Should Contain  Author and title must be at least 5 characters long

Edit With Author Too Long
    ${LONG}=    Evaluate    'a' * 301
    Create New Reference And Navigate To List Page
    Edit Reference  misc  ${LONG}  testTitle1  2025
    Page Should Contain  Author and title must be at most 300 characters long

Edit With Title Too Short
    Create New Reference And Navigate To List Page
    Edit Reference  misc  testAuthor1  Titl  2025
    Page Should Contain  Author and title must be at least 5 characters long

Edit With Title Too Long
    ${LONG}=    Evaluate    'a' * 301
    Create New Reference And Navigate To List Page
    Edit Reference  misc  testAuthor1  ${LONG}  2025
    Page Should Contain  Author and title must be at most 300 characters long

Edit With Year Too Early
    Create New Reference And Navigate To List Page
    Edit Reference  misc  testAuthor1  testTitle1  0
    Page Should Contain  Invalid year

Edit With Year Too Late
    Create New Reference And Navigate To List Page
    Edit Reference  misc  testAuthor1  testTitle1  2030
    Page Should Contain  Invalid year

Edit With Year As Text
    Create New Reference And Navigate To List Page
    Edit Reference  misc  testAuthor1  testTitle1  ysiysi
    Page Should Contain  Year must be an integer

Edit Article With Volume As Text
    Create New Reference And Navigate To List Page
    Edit Reference  article  testAuthor1  testTitle1  2020  volume=ysi
    Page Should Contain  Volume must be an integer

Edit Article With Too Long Journal
    ${LONG}=    Evaluate    'a' * 301
    Create New Reference And Navigate To List Page
    Edit Reference  article  testAuthor1  testTitle1  2020  journal=${LONG}
    Page Should Contain  Journal must be at most 300 characters

Edit Article With Too Long Pages
    ${LONG}=    Evaluate    'a' * 301
    Create New Reference And Navigate To List Page
    Edit Reference  article  testAuthor1  testTitle1  2020  pages=${LONG}
    Page Should Contain  Pages must be at most 300 characters

Edit Book With Too Long Publisher
    ${LONG}=    Evaluate    'a' * 301
    Create New Reference And Navigate To List Page
    Edit Reference  book  testAuthor1  testTitle1  2020  publisher=${LONG}
    Page Should Contain  Publisher must be at most 300 characters

Edit Inproceedings With Too Long Booktitle
    ${LONG}=    Evaluate    'a' * 301
    Create New Reference And Navigate To List Page
    Edit Reference  inproceedings  testAuthor1  testTitle1  2020  booktitle=${LONG}
    Page Should Contain  Booktitle must be at most 300 characters

*** Keywords ***
Create New Reference And Navigate To List Page
    Create Reference  book  testAuthor  testTitle  2025
    Open Reference List Page
    Click Button  Muokkaa

Submit Edit
    Click Button  Edit

Fill Edit Form
    [Arguments]  ${type}  ${author}  ${title}  ${year}  ${journal}=None  ${volume}=None  ${pages}=None  ${publisher}=None  ${booktitle}=None
    Select From List By Value  name=ref_type  ${type}
    Input Text  name=ref_author  ${author}
    Input Text  name=ref_title  ${title}
    Input Text  name=ref_year  ${year}

    Input Text If Visible  name=ref_journal  ${journal}
    Input Text If Visible  name=ref_volume  ${volume}
    Input Text If Visible  name=ref_pages  ${pages}
    Input Text If Visible  name=ref_publisher  ${publisher}
    Input Text If Visible  name=ref_booktitle  ${booktitle}

Edit Reference
    [Arguments]  ${type}  ${author}  ${title}  ${year}  ${journal}=None  ${volume}=None  ${pages}=None  ${publisher}=None  ${booktitle}=None
    Fill Edit Form  ${type}  ${author}  ${title}  ${year}  ${journal}  ${volume}  ${pages}  ${publisher}  ${booktitle}
    Submit Edit