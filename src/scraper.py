import re
from flask import flash, redirect
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from util import InvalidURLError, validate_url

def extract_title(base, is_book=False):
    if is_book:
        container = base.find('h2', {'class': 'left-bordered-title'})
        title = container.find('span')
    else:
        title = base.find('h1', {'property': 'name'})
    return title.text

def extract_doi(url):
    match = re.search(r"10\.\d+/[-._;()/:A-Z0-9]+", url)
    if match:
        return match.group()
    return False

def extract_year(base, is_book=False):
    if is_book:
        date = base.find('h2', {'class': 'left-bordered-title'}).find('span', {'class': 'date'})
        split_date = date.text.split(" ")
        return int(split_date[1])
    date = base.find('span', {'class': 'core-date-published'})
    split_date = date.text.split(" ")
    return int(split_date[2])

def extract_authors(base, is_book=False):
    authors = []
    if is_book:
        container = base.find('ul', {'title': 'list of authors'})
        for author in container.find_all('a'):
            authors.append(author.text)
    else:
        container = base.find('span', {'class': 'authors'})
        container = container.find('span', {'role': 'list'})
        for author in container.find_all('span', {'property': 'author'}):
            authors.append(author.find('a').text)
    return authors

def extract_type(base):
    cite_type = ""
    breadcrumbs = base.find('nav', {'class': 'article__breadcrumbs'})
    for link in breadcrumbs.find_all('li'):
        if link.text == "Proceedings":
            cite_type = "inproceedings"
            break
        if link.text == "Magazines":
            cite_type = "article"
            break
    if cite_type == "":
        cite_type = "misc"
    return cite_type

def extract_booktitle(base):
    container = base.find('div', {'class': 'core-self-citation'})
    info = container.find('div', {'property': 'isPartOf'})
    booktitle = info.find('a')
    return booktitle.text

def extract_publisher(base):
    container = base.find('div', {'class': 'published-info'})
    info = container.find('ul', {'class': 'rlist--inline'})
    publisher = info.find('li')
    return publisher.text

def extract_article_info(base):
    info = base.find('div', {'class': 'core-self-citation'})
    journal = info.find('span', {'property': 'name'}).text
    volume = info.find('span', {'property': 'volumeNumber'}).text
    pages = "-".join([info.find('span', {'property': 'pageStart'}).text, info.find('span', {'property': 'pageEnd'}).text])
    return {
        'journal': journal,
        'volume': volume,
        'pages': pages
    }

def extract_book_info(url, info):
    return {
        'type': 'book',
        'doi': extract_doi(url),
        'year': extract_year(info, True),
        'title': extract_title(info, True),
        'authors': extract_authors(info, True),
        'published': extract_publisher(info)
    }

def extract_base_info(url, info):
    return {
        'type': extract_type(info),
        'doi': extract_doi(url),
        'year': extract_year(info),
        'title': extract_title(info),
        'authors': extract_authors(info)
    }

def dismiss_cookies(driver):
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonDecline"))
    )
    cookie_button.click()

def expand_book_authors(driver):
    if driver.find_element(By.CLASS_NAME, 'count-list'):
        expand_authors_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "count-list"))
        )
        expand_authors_button.click()

def retrieve_info_container(soup, driver, is_book):
    if is_book:
        WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME, 'container')) )
        dismiss_cookies(driver)
        expand_book_authors(driver)
        return soup.find('div', {'class': 'colored-block'})
    WebDriverWait(driver, 10).until( EC.presence_of_element_located((By.CLASS_NAME, 'core-container')) )
    return soup.find('div', {'class': 'core-container'})

def scrape_acm(url: str):
    try:
        validate_url(url)

        headers = 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.166 Safari/537.36'
        options = Options()
        options.add_argument('--headless=new')
        options.add_argument(f'user-agent={headers}')

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        soup = bs(driver.page_source, 'lxml')
        data = {}

        is_book = "book" in url
        info = retrieve_info_container(soup, driver, is_book)

        if is_book:
            data = extract_book_info(url, info)
        else:
            data = extract_base_info(url, info)

            if data['type'] == "article":
                article_data = extract_article_info(info)
                data.update(article_data)
            elif data['type'] == "inproceedings":
                data['booktitle'] = extract_booktitle(info)

        driver.quit()
        return data

    except InvalidURLError as e:
        flash(str(e), "error")
        return redirect("/new_ref")
