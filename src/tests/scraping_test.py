import unittest
from scraper import scrape_acm

class TestScraper(unittest.TestCase):
    def test_scraper_returns_book_info(self):
        url = "https://dl.acm.org/doi/book/10.1145/3277669"
        data = scrape_acm(url)
        self.assertEqual(data['type'], "book")
        self.assertEqual(data['doi'], "10.1145/3277669")
        self.assertEqual(data['year'], 2019)
        self.assertEqual(data['title'], "The Essentials of Modern Software Engineering: Free the Practices from the Method Prisons!")
        self.assertEqual(data['authors'], ['Ivar Jacobson', 'Harold "Bud" Lawson', 'Pan-Wei Ng', 'Paul E. McMahon', 'Michael Goedicke'])
        self.assertEqual(data['published'], "Association for Computing Machinery and Morgan & Claypool")

    def test_scraper_returns_inproceedings_info(self):
        url = "https://dl.acm.org/doi/10.1145/3544548.3581318"
        data = scrape_acm(url)
        self.assertEqual(data['type'], 'inproceedings')
        self.assertEqual(data['doi'], '10.1145/3544548.3581318')
        self.assertEqual(data['year'], 2023)
        self.assertEqual(data['title'], 'Synthetic Lies: Understanding AI-Generated Misinformation and Evaluating Algorithmic and Human Solutions')
        self.assertEqual(data['authors'], ['Jiawei Zhou', 'Yixuan Zhang', 'Qianni Luo', 'Andrea G Parker', 'Munmun De Choudhury'])
        self.assertEqual(data['booktitle'], "CHI '23: Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems")

    def test_scraper_returns_article_info(self):
        url = "https://dl.acm.org/doi/10.1145/3746661"
        data = scrape_acm(url)
        self.assertEqual(data['type'], 'article')
        self.assertEqual(data['doi'], '10.1145/3746661')
        self.assertEqual(data['year'], 2025)
        self.assertEqual(data['title'], 'THINKING ISSUES: Future(s) Within Academic Computing')
        self.assertEqual(data['authors'], ['Randy Connolly'])
        self.assertEqual(data['journal'], 'ACM Inroads')
        self.assertEqual(data['volume'], '16')
        self.assertEqual(data['pages'], '6-10')
