import unittest
from config import app, db
from db_helper import setup_db, reset_db
from repositories.citation_repository import get_citations, create_ref


class TestGetCitations(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()

    def tearDown(self):
        with app.app_context():
            reset_db()
            db.session.remove()

    def test_get_empty_citations(self):
        with app.app_context():
            result = get_citations()
            self.assertEqual(len(result["items"]), 0)
            self.assertEqual(result["total"], 0)

    def test_create_and_get_citation(self):
        with app.app_context():
            create_ref("article", "John Doe", "Test Article", 2020)
            result = get_citations()
            self.assertEqual(len(result["items"]), 1)
            self.assertEqual(result["items"][0].title, "Test Article")
            self.assertEqual(result["items"][0].author, "John Doe")
            self.assertEqual(result["items"][0].type, "article")
            self.assertEqual(result["items"][0].year, 2020)

    def test_get_multiple_citations(self):
        with app.app_context():
            create_ref("article", "John Doe", "Test Article", 2020)
            create_ref("book", "Jane Smith", "Test Book", 2021)
            create_ref("inproceedings", "Bob Johnson", "Conference Paper", 2022)
            result = get_citations()
            self.assertEqual(result["total"], 3)
            self.assertEqual(len(result["items"]), 3)

    def test_get_citations_filtered_by_type(self):
        with app.app_context():
            base = {"query":"", "type":""}
            create_ref("article", "John Doe", "Test Article", 2020)
            create_ref("book", "Jane Smith", "Test Book", 2021)
            create_ref("book", "Jane Smith", "Test Book", 2021)
            self.assertEqual(get_citations(filters={**base, "type":"book"})["total"], 2)
            self.assertEqual(get_citations(filters={**base, "type":"article"})["total"], 1)
            self.assertEqual(get_citations(filters={**base, "type":"inproceedings"})["total"], 0)
            self.assertEqual(get_citations(filters={**base, "type":"book"})["pages"], 1)
            self.assertEqual(get_citations(filters={**base, "type":"misc"})["pages"], 0)

    def test_get_citations_filtered_by_query(self):
        with app.app_context():
            base = {"query":"", "type":""}
            create_ref("article", "John Doe", "Article", 2020)
            create_ref("book", "Jane Smith", "Programming 101", 2021)
            create_ref("inproceedings", "Bob Johnson", "Inproceedings", 2022)
            self.assertEqual(get_citations(filters={**base, "query":"10"})["total"], 1)
            self.assertEqual(get_citations(filters={**base, "query":"pro"})["total"], 2)
            self.assertEqual(get_citations(filters={**base, "query":"John"})["total"], 2)
            self.assertEqual(get_citations(filters={**base, "query":":)"})["total"], 0)
            self.assertEqual(get_citations(filters={**base, "query":"Pro"})["pages"], 1)
            self.assertEqual(get_citations(filters={**base, "query":":)"})["pages"], 0)

    def test_pagination(self):
        with app.app_context():
            create_ref("article", "Author 1", "Title 1", 2020)
            create_ref("book", "Author 2", "Title 2", 2021)
            create_ref("inproceedings", "Author 3", "Title 3", 2022)
            
            result = get_citations(page=1, per_page=2)
            self.assertEqual(len(result["items"]), 2)
            self.assertEqual(result["page"], 1)
            self.assertEqual(result["total"], 3)
            self.assertEqual(result["pages"], 2)
            
            result = get_citations(page=2, per_page=2)
            self.assertEqual(len(result["items"]), 1)
            self.assertEqual(result["page"], 2)


if __name__ == "__main__":
    unittest.main()
