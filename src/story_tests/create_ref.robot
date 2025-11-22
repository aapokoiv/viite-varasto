*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs

*** Test Cases ***

Create Article Reference Successfully With No Optional Fields
    Create Reference  article  Miquel  Artikkelin testaus   2020
    No Error Messages

Create Article Reference Successfully With All Optional Fields
    Create Reference  article  Miquel  Artikkelin testaus  2020  Journal  10  32-36
    No Error Messages

Create Article Reference Successfully With Some Optional Fields
    Create Reference  article  Miquel  Artikkelin testaus  2020  volume=10
    No Error Messages

Create Article With Too Long Journal
    ${LONG}=    Evaluate    'a' * 301
    Create Reference  article  Author  Title  2020  journal=${LONG}
    Page Should Contain  Journal must be at most 300 characters long

Create Article With Too Long Pages
    ${LONG}=    Evaluate    'a' * 301
    Create Reference  article  Author  Title  2020  pages=${LONG}
    Page Should Contain  Pages must be at most 300 characters long

Create Article With Non-integer Volume
    Create Reference  article  Maija  Testi  2020  volume=kybä
    Page Should Contain  Volume must be an integer

Create Book Reference Successfully With No Optional Field
    Create Reference  book  Matti Meikäläinen  Kirjan testaus  2018 
    No Error Messages

Create Book Reference Successfully With Optional Field
    Create Reference  book  Matti Meikäläinen  Kirjan testaus  2018  publisher=publisher
    No Error Messages

Create Book With Too Long Publisher
    ${LONG}=    Evaluate    'a' * 301
    Create Reference  book  Author  Title  2020  publisher=${LONG}
    Page Should Contain  Publisher must be at most 300 characters long

Create Inproceedings Reference Successfully With No Optional Field
    Create Reference  inproceedings  Maija Mehiläinen  Konferenssijulkaisun testaus  2019
    No Error Messages

Create Inproceedings Reference Successfully With Optional Field
    Create Reference  inproceedings  Maija Mehiläinen  Konferenssijulkaisun testaus  2019  booktitle=booktitle
    No Error Messages

Create Inproceedings Reference With Too Long Booktitle
    ${LONG}=    Evaluate    'a' * 301
    Create Reference  inproceedings  Maija Mehiläinen  Konferenssijulkaisun testaus  2019  booktitle=${LONG}
    Page Should Contain  Booktitle must be at most 300 characters long

Create Misc Reference Successfully
    Create Reference  misc  Jukka Poika  Todella kaunis runo  1800
    No Error Messages

Create Reference With Too Short Author
    Create Reference  book  Kia  Testikirja  2020
    Page Should Contain  Author and title must be at least 5 characters long

Create Reference With Too Short Title
    Create Reference  article  Pekka  Jouu  2021
    Page Should Contain  Author and title must be at least 5 characters long

Create Reference With Too Long Author
    ${LONG}=    Evaluate    'a' * 301
    Create Reference  article  ${LONG}  Testi  2020
    Page Should Contain  Author and title must be at most 300 characters long

Create Reference With Too Long Title
    ${LONG}=    Evaluate    'a' * 301
    Create Reference  book  Pekka  ${LONG}  2019
    Page Should Contain  Author and title must be at most 300 characters long

Create Reference With Non-integer Year
    Create Reference  misc  Maija  Testi  year2020
    Page Should Contain  Year must be an integer

Create Reference With Year Too Small
    Create Reference  inproceedings  Matti  Testi  0
    Page Should Contain  Invalid year

Create Reference With Year Too Large
    Create Reference  article  Jukka  Testi  2027
    Page Should Contain  Invalid year

