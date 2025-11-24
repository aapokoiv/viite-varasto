*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs

*** Test Cases ***

Create Article Reference Successfully With No Optional Fields
    Create Reference  article  art-kw  Miquel  Artikkelin testaus   2020
    No Error Messages

Create Article Reference Successfully With All Optional Fields
    Create Reference  article  art-kw  Miquel  Artikkelin testaus  2020  Journal  10  32-36
    No Error Messages

Create Article Reference Successfully With Some Optional Fields
    Create Reference  article  art-kw  Miquel  Artikkelin testaus  2020  volume=10
    No Error Messages

Create Article With Non-integer Volume
    Create Reference  article  art-kw  Maija  Testi  2020  volume=kybä
    Page Should Contain  Volume must be an integer

Create Book Reference Successfully With No Optional Field
    Create Reference  book  art-kw  Matti Meikäläinen  Kirjan testaus  2018 
    No Error Messages

Create Book Reference Successfully With Optional Field
    Create Reference  book  art-kw  Matti Meikäläinen  Kirjan testaus  2018  publisher=publisher
    No Error Messages

Create Inproceedings Reference Successfully With No Optional Field
    Create Reference  inproceedings  art-kw  Maija Mehiläinen  Konferenssijulkaisun testaus  2019
    No Error Messages

Create Inproceedings Reference Successfully With Optional Field
    Create Reference  inproceedings  art-kw  Maija Mehiläinen  Konferenssijulkaisun testaus  2019  booktitle=booktitle
    No Error Messages

Create Misc Reference Successfully
    Create Reference  misc  misc-kw  Jukka Poika  Todella kaunis runo  1800
    No Error Messages

Create Reference With Too Short Author
    Create Reference  book  short-kw  Ki  Testikirja  2020
    Page Should Contain  Author and title must be at least 3 characters long

Create Reference With Too Short Title
    Create Reference  article  short-kw  Pekka  Jo  2021
    Page Should Contain  Author and title must be at least 3 characters long

Create Reference With Non-integer Year
    Create Reference  misc  year-kw  Maija  Testi  year2020
    Page Should Contain  Year must be an integer

Create Reference Notification Is Displayed On Screen
    Create Reference  misc  year-kw  Maija  Testi  22
    Page Should Contain  Reference succesfully created.
