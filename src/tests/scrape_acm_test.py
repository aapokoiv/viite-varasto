import unittest
from scraper import scrape_acm
from config import app
from db_helper import setup_db, reset_db

class TestScrapeACM(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()

    def tearDown(self):
        with app.app_context():
            reset_db()

    def test_scrape_acm_article(self):
        url = "https://dl.acm.org/doi/10.1145/3368089.3409732"
        data = scrape_acm(url)
        
        self.assertIsInstance(data, dict)
        expected_keys = {'type', 'doi', 'year', 'title', 'authors'}
        self.assertTrue(expected_keys.issubset(set(data.keys())))
        
        self.assertIn(data['type'], ['article', 'inproceedings', 'misc', 'book'])
        
        self.assertIsNotNone(data.get('title'))
        self.assertIsNotNone(data.get('authors'))
        self.assertTrue(len(data.get('title', '')) > 0)

    def test_scrape_acm_returns_dict(self):
        url = "https://dl.acm.org/doi/10.1145/3368089.3409732"
        data = scrape_acm(url)
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)
    

    def test_scrape_acm_inproceedings(self):
        """Test that scrape_acm can handle conference proceedings"""
        url = "https://dl.acm.org/doi/10.1145/3377811.3380362"
        data = scrape_acm(url)
        
        if data is None:
            self.skipTest("Could not scrape the ACM URL - website may have changed")
        
        self.assertIsInstance(data, dict)
        
        self.assertIn('type', data)
        self.assertIn('title', data)
        
        self.assertIn(data.get('type'), ['article', 'inproceedings', 'misc', 'book'])
        
        self.assertTrue(len(data.get('title', '')) > 0)


    def test_scrape_acm_invalid_url(self):
        url = "https://dl.acm.org/doi/invalid"
        with self.assertRaises(Exception):
            scrape_acm(url)