import unittest
from bs4 import BeautifulSoup as bs
from unittest.mock import MagicMock, patch
from scraper import (
    extract_title, extract_doi, extract_year, extract_authors,
    extract_type, extract_booktitle, extract_publisher,
    extract_article_info, dismiss_cookies, expand_book_authors,
    retrieve_info_container, scrape_acm
)


class TestScraper(unittest.TestCase):
    def test_extract_title_returns_correct_on_article(self):
        html = '<h1 property="name">TestTitle</h1>'
        soup = bs(html, 'lxml')
        data = extract_title(soup)
        self.assertEqual(data, "TestTitle")

    def test_extract_title_returns_correct_on_book(self, ):
        html = '<h2 class="left-bordered-title"><span>TestBookTitle</span></h2>'
        soup = bs(html, 'lxml')
        data = extract_title(soup, True)
        self.assertEqual(data, "TestBookTitle")

    def test_extract_doi_returns_correct(self):
        url = "https://dl.acm.org/doi/10.1145/2380552.2380613"
        url2 = "https://dl.acm.org/doi/book/10.1145/3705572"
        data = extract_doi(url)
        data2 = extract_doi(url2)
        self.assertEqual(data, "10.1145/2380552.2380613")
        self.assertEqual(data2, "10.1145/3705572")

    def test_extract_doi_returns_incorrect(self):
        url = "https://dl.acm.org/doi/Moi/2380552.2380613"
        url2 = "https://dl.acm.org/doi/book/Moi/3705572"
        data = extract_doi(url)
        data2 = extract_doi(url2)
        self.assertEqual(data, False)
        self.assertEqual(data2, False)

    def test_extract_year_article(self):
        html = '<span class="core-date-published">27 March 2020</span>'
        data = bs(html, 'lxml')
        self.assertEqual(extract_year(data), 2020)

    def test_extract_year_book(self):
        html = '<h2 class="left-bordered-title"><span class="date">March 2018</span></h2>'
        data = bs(html, 'lxml')
        self.assertEqual(extract_year(data, is_book=True), 2018)

    def test_extract_authors_article(self):
        html = '''
        <span class="authors">
          <span role="list">
            <span property="author"><a>Author One</a></span>
            <span property="author"><a>Author Two</a></span>
          </span>
        </span>
        '''
        data = bs(html, 'lxml')
        self.assertEqual(extract_authors(data), ["Author One", "Author Two"])

    def test_extract_authors_book(self):
        html = '''
        <ul title="list of authors">
          <li><a>Author A</a></li>
          <li><a>Author B</a></li>
        </ul>
        '''
        data = bs(html, 'lxml')
        self.assertEqual(extract_authors(data, is_book=True), ["Author A", "Author B"])

    def test_extract_type_proceedings(self):
        html = '<nav class="article__breadcrumbs"><li>Proceedings</li></nav>'
        data = bs(html, 'lxml')
        self.assertEqual(extract_type(data), "inproceedings")

    def test_extract_type_magazine(self):
        html = '<nav class="article__breadcrumbs"><li>Magazines</li></nav>'
        data = bs(html, 'lxml')
        self.assertEqual(extract_type(data), "article")

    def test_extract_type_misc(self):
        html = '<nav class="article__breadcrumbs"><li>Other</li></nav>'
        data = bs(html, 'lxml')
        self.assertEqual(extract_type(data), "misc")

    def test_extract_article_info(self):
        html = '''
        <div class="core-self-citation">
          <span property="name">Journal Name</span>
          <span property="volumeNumber">42</span>
          <span property="pageStart">10</span>
          <span property="pageEnd">20</span>
        </div>
        '''
        data = bs(html, 'lxml')
        expected = {'journal': 'Journal Name', 'volume': '42', 'pages': '10-20'}
        self.assertEqual(extract_article_info(data), expected)

    def test_extract_booktitle(self):
        html = '<div class="core-self-citation"><div property="isPartOf"><a>BooktitleTest</a></div></div>'
        data = bs(html, 'lxml')
        self.assertEqual(extract_booktitle(data), "BooktitleTest")

    def test_extract_publisher(self):
        html = '<div class="published-info"><ul class="rlist--inline"><li>PublisherTest</li></ul></div>'
        data = bs(html, 'lxml')
        self.assertEqual(extract_publisher(data), "PublisherTest")

    @patch("scraper.WebDriverWait")
    def test_dismiss_cookies_clicks_button(self, mock_wait):
        fake_button = MagicMock()
        mock_wait.return_value.until.return_value = fake_button

        driver = MagicMock()
        dismiss_cookies(driver)

        fake_button.click.assert_called_once()

    @patch("scraper.WebDriverWait")
    def test_expand_book_authors_clicks_button(self, mock_wait):
        driver = MagicMock()
        driver.find_element.return_value = True
        fake_button = MagicMock()
        mock_wait.return_value.until.return_value = fake_button

        from scraper import expand_book_authors
        expand_book_authors(driver)

        fake_button.click.assert_called_once()

    @patch("scraper.WebDriverWait")
    @patch("scraper.dismiss_cookies")
    @patch("scraper.expand_book_authors")
    def test_retrieve_info_container_book(self, mock_expand, mock_dismiss, mock_wait):
        html = '<div class="colored-block">Book Info</div>'
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')

        driver = MagicMock()
        result = retrieve_info_container(soup, driver, is_book=True)

        self.assertEqual(result.text, "Book Info")
        mock_dismiss.assert_called_once_with(driver)
        mock_expand.assert_called_once_with(driver)

    @patch("scraper.WebDriverWait")
    def test_retrieve_info_container_article(self, mock_wait):
        html = '<div class="core-container">Article Info</div>'
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'lxml')

        driver = MagicMock()
        result = retrieve_info_container(soup, driver, is_book=False)

        self.assertEqual(result.text, "Article Info")

    @patch("scraper.validate_url")
    @patch("scraper.webdriver.Chrome")
    def test_scrape_acm_article(self, mock_chrome, mock_validate):
        mock_validate.return_value = True
        driver = MagicMock()
        driver.page_source = '<div class="core-container"><h1 property="name">TestTitle</h1><span class="core-date-published">Published March 2020</span><span class="authors"><span role="list"><span property="author"><a>Author One</a></span></span></span><nav class="article__breadcrumbs"><li>Magazines</li></nav><div class="core-self-citation"><span property="name">Journal</span><span property="volumeNumber">42</span><span property="pageStart">10</span><span property="pageEnd">20</span></div></div>'
        mock_chrome.return_value = driver

        result = scrape_acm("http://example.com/article")
        self.assertEqual(result["title"], "TestTitle")
        self.assertEqual(result["year"], 2020)
        self.assertEqual(result["authors"], ["Author One"])
        self.assertEqual(result["type"], "article")
        self.assertEqual(result["journal"], "Journal")