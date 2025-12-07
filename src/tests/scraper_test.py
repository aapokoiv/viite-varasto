import unittest
from bs4 import BeautifulSoup as bs
from scraper import (
    extract_title, extract_doi, extract_year, extract_authors,
    extract_type, extract_booktitle, extract_publisher,
    extract_article_info, extract_book_info, extract_base_info,
    dismiss_cookies, expand_book_authors, retrieve_info_container,
    scrape_acm
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
