import unittest
from config import app, db
from db_helper import setup_db, reset_db
from repositories.citation_repository import get_citations, create_ref, get_citation_by_id, delete_ref

class TestDeleteRef(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()
    
    def tearDown(self):
        with app.app_context():
            reset_db()
            db.session.remove()
    
    def test_delete_ref_successfully_removes_entry(self):
        with app.app_context():
            create_ref("article", "test_kw", "John Doe", "Sample Title", 2020)
            result = get_citations()
            ref_id = result["items"][0].id
            delete_ref(ref_id)
            deleted = get_citation_by_id(ref_id)
            self.assertIsNone(deleted)
        
    def test_delete_reduces_total_count(self):
        with app.app_context():
            create_ref("article", "test_kw1", "John Doe", "Sample Title 1", 2020)
            create_ref("book", "test_kw2", "Jane Smith", "Sample Title 2", 2021)
            result_before = get_citations()
            total_before = result_before["total"]
            ref_id = result_before["items"][0].id
            delete_ref(ref_id)
            result_after = get_citations()
            total_after = result_after["total"]
            self.assertEqual(total_before - 1, total_after)
    
    def test_delete_nonexistent_ref_does_not_raise_error(self):
        with app.app_context():
            create_ref("article", "test_kw", "John Doe", "Sample Title", 2020)
            before_count = get_citations()["total"]
            try:
                delete_ref(999999)
            except Exception as e:
                self.fail(f"delete_ref raised an exception unexpectedly: {e}")
            after_count = get_citations()["total"]
            self.assertEqual(before_count, after_count)
    
if __name__ == "__main__":
    unittest.main()