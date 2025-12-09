# User can filter the reference list by Year through a range input
# User can filter the reference list by Category
# User can filter the reference list by Type
# Multiple filters can be applied at the same time.

*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Reset Refs


*** Test Cases ***

Page Lists References Filtered By Type
    Create Reference  article  kw1  Matti  Ensimmäinen artikkeli  2000  doi=10.6000/kw1  category=TypeArt
    Create Reference  book  kw2  Jukka  Toinen kirja  2010  doi=10.6000/kw2  category=TypeBook
    Open Reference List Page
    Filter References By Selection  type  book
    Page Should Contain  Jukka
    Page Should Not Contain  Matti

Page Lists References Filtered By Search
    Create Reference  article  kw1  Matti  Ensimmäinen artikkeli  2000  doi=10.6010/s1  category=SearchArt
    Create Reference  book  kw2  Jukka  Toinen kirja  2010  doi=10.6010/s2  category=SearchBook
    Open Reference List Page
    Filter References By Search  Ensimmäinen
    Page Should Contain  Matti
    Page Should Not Contain  Jukka

Page Lists References Filtered By Year
    Create Reference  article  kw1  Matti  Ensimmäinen artikkeli  2008  doi=10.6020/y1  category=YearArt
    Create Reference  book  kw2  Jukka  Toinen kirja  2014  doi=10.6020/y2  category=YearBook
    Create Reference  book  kw3  Jukka  Kolmas kirja  1972  doi=10.6020/y3  category=YearBook
    Create Reference  book  kw4  Jukka  Neljäs kirja  1968  doi=10.6020/y4  category=YearBook
    Open Reference List Page
    Filter References By Year  year-from  400  year-to  1990
    Page Should Contain  1972
    Page Should Contain  1968
    Page Should Not Contain  2008
    Page Should Not Contain  2014

Page Lists References Filtered By Category
    Create Reference  article  kw1  Matti  Ensimmäinen artikkeli  2008  doi=10.6020/y1  category=YearArt
    Create Reference  book  kw2  Jukka  Toinen kirja  2014  doi=10.6020/y2  category=YearBook
    Create Reference  book  kw3  Jukka  Kolmas kirja  1972  doi=10.6020/y3  category=YearBook
    Create Reference  book  kw4  Jukka  Neljäs kirja  1968  doi=10.6020/y4  category=YearBook
    Open Reference List Page
    Filter References By Category  YearBook
    Page Should Contain  2014
    Page Should Contain  1972
    Page Should Contain  1968
    Page Should Not Contain  2008
