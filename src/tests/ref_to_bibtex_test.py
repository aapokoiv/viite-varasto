import unittest
from config import app, db
from db_helper import setup_db, reset_db
from repositories.citation_repository import create_ref, get_all_citations
from repositories.bibtex_repository import all_citations_to_bibtex

class TestBibtexExport(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()

    def tearDown(self):
        with app.app_context():
            reset_db()
            db.session.remove()

    def test_all_citations_to_bibtex(self):
        with app.app_context():
            create_ref("article", "test_kw", "John Doe", "Test Article", 2020, journal="Test Journal", volume="1", pages="1-10")
            bibtex_data = all_citations_to_bibtex()
            expected_bibtex = (
                "@article{test_kw,\n"
                "  author = {John Doe},\n"
                "  title = {Test Article},\n"
                "  year = {2020},\n"
                "  journal = {Test Journal},\n"
                "  volume = {1},\n"
                "  pages = {1-10}\n"
                "}"
            )
            self.assertEqual(bibtex_data.strip(), expected_bibtex.strip())

    def test_all_citations_to_bibtex_empty(self):
        with app.app_context():
            bibtex_data = all_citations_to_bibtex()
            self.assertEqual(bibtex_data, "")

if __name__ == "__main__":
        unittest.main()