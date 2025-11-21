*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs

*** Test Cases ***

Create Article Reference Successfully
    Create Reference  article  art-kw  Miquel  Artikkelin testaus   2020
    No Error Messages

Create Book Reference Successfully
    Create Reference  book  book-kw  Matti Meikäläinen  Kirjan testaus  2018 
    No Error Messages

Create Inproceedings Reference Successfully
    Create Reference  inproceedings  conf-kw  Maija Mehiläinen  Konferenssijulkaisun testaus  2019
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

