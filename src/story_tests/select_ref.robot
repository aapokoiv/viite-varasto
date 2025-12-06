*** Settings ***
Resource  resource.robot
Library  RequestsLibrary
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs

*** Test Cases ***

Access Select References Page
    Create Reference  article  bibtex-kw  BibTeX Author  BibTeX  2021  doi=10.1234/abc  category=BibCategory  journal=Journal  volume=5  pages=100-110
    Open Reference List Page
    Click Button  Valitse viitteet BibTeX-tiedostoon
    Page Should Contain  Valitse viitteet BibTeX-tiedostoon
    Page Should Contain Element  class=refs-table
    Element Should Be Visible  id=category-filter

References Without Category Are Visible
    Create Reference  article  bibtex-kw  BibTeX Author  BibTeX  2021
    Open Select References Page
    Page Should Contain  BibTeX

Filter References By Category
    Create Reference  article  bibtex-kw1  Author One  Title One  2021  category=CatA
    Create Reference  book  bibtex-kw2  Author Two  Title Two  2022  category=CatB
    Open Select References Page
    Select From List By Value  id=category-filter  CatA
    Page Should Contain  Title One
    Page Should Not Contain  Title Two

Select All References In Category
    Create Reference  article  bibtex-kw1  Author One  Title One  2021  category=CatA
    Create Reference  book  bibtex-kw2  Author Two  Title Two  2022  category=CatA
    Open Select References Page
    Select From List By Value  id=category-filter  CatA
    Click Button  Valitse kaikki näkyvät
    Checkbox Should Be Selected  xpath=//tr[td[normalize-space(text())='Title One']]/td/input[@type='checkbox']
    Checkbox Should Be Selected  xpath=//tr[td[normalize-space(text())='Title Two']]/td/input[@type='checkbox']

Select Individual References
    Create Reference  article  bibtex-kw1  Author One  Title One  2021  category=CatA
    Create Reference  book  bibtex-kw2  Author Two  Title Two  2022  category=CatA
    Open Select References Page
    Select From List By Value  id=category-filter  CatA
    Click Element  xpath=//tr[td[normalize-space(text())='Title One']]/td/input[@type='checkbox']
    Checkbox Should Be Selected  xpath=//tr[td[normalize-space(text())='Title One']]/td/input[@type='checkbox']
    Checkbox Should Not Be Selected  xpath=//tr[td[normalize-space(text())='Title Two']]/td/input[@type='checkbox']

Cannot Export Without Selecting Reference
    Create Reference  article  bibtex-kw1  Author One  Title One  2021  category=CatA
    Open Select References Page
    Click Button  Lataa valitut BibTeX
    Page Should Contain  No references selected for export

Go Back To Reference List From Select Page
    Open Select References Page
    Click Button  Takaisin viitelistaan
    Page Should Contain  View all the references

Export Multiple Selected References
    Create Reference  article  bibtex-kw1  Author One  Title One  2021  category=CatA  journal=Journal A  volume=1  pages=1-10
    Create Reference  book  bibtex-kw2  Author Two  Title Two  2022  category=CatA  publisher=Publisher B
    Open Select References Page
    Click Element  xpath=//tr[td[normalize-space(text())='Title One']]/td/input[@type='checkbox']
    Click Element  xpath=//tr[td[normalize-space(text())='Title Two']]/td/input[@type='checkbox']
    Click Button  Lataa valitut BibTeX
    Page Should Not Contain  No references selected for export

*** Keywords ***
Open Select References Page
    Go To  ${REF_SELECT_URL}
    Wait Until Page Contains Element  class=refs-table  30 seconds