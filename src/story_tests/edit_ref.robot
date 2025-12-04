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
    Edit Reference  misc  misc-kw  testAuthor1  testTitle1  2024
    No Error Messages

Edit Article With Correct Inputs And Optional Fields
    Create New Reference And Navigate To List Page
    Edit Reference  article  art-kw  testAuthor1  testTitle1  2024  doi=10.1111/editart  category=EditArticleCat  journal=journal  volume=1  pages=32-34
    No Error Messages

Edit Book With Correct Inputs And Optional Field
    Create New Reference And Navigate To List Page
    Edit Reference  book  book-kw  testAuthor1  testTitle1  2024  doi=10.2222/editbook  category=EditBookCat  publisher=publisher
    No Error Messages

Edit Inproceedings With Correct Inputs And Optional Field
    Create New Reference And Navigate To List Page
    Edit Reference  inproceedings  inprc-kw  testAuthor1  testTitle1  2024  doi=10.3333/editconf  category=EditConfCat  booktitle=booktitle
    No Error Messages

Edit With Author Too Short
    Create New Reference And Navigate To List Page
    Edit Reference  misc  misc-kw  Au  testTitle1  2025
    Page Should Contain  Author and title must be at least 3 characters long

Edit With Title Too Short
    Create New Reference And Navigate To List Page
    Edit Reference  misc  misc-kw  testAuthor1  T  2025
    Page Should Contain  Author and title must be at least 3 characters long

Edit With Year As Text
    Create New Reference And Navigate To List Page
    Edit Reference  misc  misc-kw  testAuthor1  testTitle1  ysiysi
    Page Should Contain  Year must be an integer

Edit Article With Volume As Text
    Create New Reference And Navigate To List Page
    Edit Reference  article  art-kw  testAuthor1  testTitle1  2020  volume=ysi
    Page Should Contain  Volume must be an integer

Edit Reference Notification Is Displayed On Screen
    Create New Reference And Navigate To List Page
    Edit Reference  article  art-kw  testAuthor1  testTitle1  2020
    Page Should Contain  Reference succesfully edited.


*** Keywords ***
Create New Reference And Navigate To List Page
    Create Reference  book  test_kw  testAuthor  testTitle  2025
    Open Reference List Page
    Click Button  Muokkaa

Submit Edit
    Click Button  Edit

Fill Edit Form
    [Arguments]  ${type}  ${keyword}  ${author}  ${title}  ${year}  ${doi}=None  ${category}=None  ${journal}=None  ${volume}=None  ${pages}=None  ${publisher}=None  ${booktitle}=None
    Select From List By Value  id=ref_type    ${type}
    Input Text  name=ref_keyword  ${keyword}
    Input Text  name=ref_author  ${author}
    Input Text  name=ref_title  ${title}
    Input Text  name=ref_year  ${year}

    Input Text If Visible  name=ref_doi  ${doi}
    Input Text If Visible  name=ref_category  ${category}
    Input Text If Visible  name=ref_journal  ${journal}
    Input Text If Visible  name=ref_volume  ${volume}
    Input Text If Visible  name=ref_pages  ${pages}
    Input Text If Visible  name=ref_publisher  ${publisher}
    Input Text If Visible  name=ref_booktitle  ${booktitle}

Edit Reference
    [Arguments]  ${type}  ${keyword}  ${author}  ${title}  ${year}  ${doi}=None  ${category}=None  ${journal}=None  ${volume}=None  ${pages}=None  ${publisher}=None  ${booktitle}=None
    Fill Edit Form  ${type}  ${keyword}  ${author}  ${title}  ${year}  ${doi}  ${category}  ${journal}  ${volume}  ${pages}  ${publisher}  ${booktitle}
    Submit Edit