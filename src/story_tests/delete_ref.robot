# User can delete a reference
# After deletion the deleted reference isn't shown on the list of references
# A notification is displayed to the user after a reference is successfully deleted

*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs

*** Test Cases ***
Delete Reference Successfully
    Create Reference  article  del-kw  del-author  del-title  2000  doi=10.4000/del  category=DelCat  journal=journal  volume=1  pages=10-20
    Open Reference List Page
    Click Delete Button  del-title
    Page Should Contain  No references found yet

Delete Right Reference Successfully
    Create Reference  article  keep-kw  keep-author  keep-title  2000  doi=10.4000/keep  category=KeepCat  journal=journal  volume=1  pages=10-20
    Create Reference  book  delete-kw  delete-author  delete-title  2010  doi=10.4000/delete  category=DeleteCat  publisher=publisher  volume=2  pages=30-40
    Open Reference List Page
    Click Delete Button  delete-title
    Page Should Not Contain  delete-title
    Page Should Contain  keep-title

Delete Reference Notification Is Displayed On Screen
    Create Reference  book  delete-kw  delete-author  delete-title  2010  doi=10.4000/delete  category=DeleteCat  publisher=publisher  volume=2  pages=30-40
    Open Reference List Page
    Click Delete Button  delete-title
    Page Should Contain  Reference succesfully deleted.


*** Keywords ***
Click Delete Button
    [Arguments]  ${title}
    Click Button  xpath=//tr[td[normalize-space(text())='${title}']]//form[contains(@action,'/delete_ref')]//input[@type='submit' and normalize-space(@value)='Poista']