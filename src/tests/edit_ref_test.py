import unittest
from config import app, db
from db_helper import setup_db, reset_db
from repositories.citation_repository import get_citations, create_ref, get_citation_by_id, update_ref


class TestEditRef(unittest.TestCase):
    def setUp(self):
        """Set up test database before each test"""
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()
            # Create a test reference to edit
            create_ref("article", "test_kw", "John Doe", "Original Title", 2020)

    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            reset_db()
            db.session.remove()

    def test_update_author_successfully(self):
        """Test updating only the author"""
        with app.app_context():
            result = get_citations()
            ref_id = result["items"][0].id
            
            update_ref(ref_id, "Jane Smith", "Original Title", 2020, "test_kw")
            
            updated_ref = get_citation_by_id(ref_id)
            self.assertEqual(updated_ref.author, "Jane Smith")

    def test_update_title_successfully(self):
        """Test updating only the title"""
        with app.app_context():
            result = get_citations()
            ref_id = result["items"][0].id
            
            update_ref(ref_id, "John Doe", "New Title", 2020, "test_kw")
            
            updated_ref = get_citation_by_id(ref_id)
            self.assertEqual(updated_ref.title, "New Title")

    def test_update_year_successfully(self):
        """Test updating only the year"""
        with app.app_context():
            result = get_citations()
            ref_id = result["items"][0].id
            
            update_ref(ref_id, "John Doe", "Original Title", 2021, "test_kw")
            
            updated_ref = get_citation_by_id(ref_id)
            self.assertEqual(updated_ref.year, 2021)

    def test_update_keyword_successfully(self):
        """Test updating only the keyword"""
        with app.app_context():
            result = get_citations()
            ref_id = result["items"][0].id
            
            update_ref(ref_id, "John Doe", "Original Title", 2020, "new_kw")
            
            updated_ref = get_citation_by_id(ref_id)
            self.assertEqual(updated_ref.keyword, "new_kw")

    def test_update_all_fields_successfully(self):
        """Test updating all fields at once"""
        with app.app_context():
            result = get_citations()
            ref_id = result["items"][0].id
            
            update_ref(ref_id, "Jane Smith", "Updated Title", 2021, "new_kw")
            
            updated_ref = get_citation_by_id(ref_id)
            self.assertEqual(updated_ref.author, "Jane Smith")
            self.assertEqual(updated_ref.title, "Updated Title")
            self.assertEqual(updated_ref.year, 2021)
            self.assertEqual(updated_ref.keyword, "new_kw")

    def test_get_citation_by_id_returns_citation(self):
        """Test retrieving a specific citation by ID"""
        with app.app_context():
            result = get_citations()
            ref_id = result["items"][0].id
            
            citation = get_citation_by_id(ref_id)
            self.assertIsNotNone(citation)
            self.assertEqual(citation.author, "John Doe")

    def test_get_nonexistent_citation_returns_none(self):
        """Test retrieving a citation that doesn't exist"""
        with app.app_context():
            citation = get_citation_by_id(9999)
            self.assertIsNone(citation)


if __name__ == "__main__":
    unittest.main()
