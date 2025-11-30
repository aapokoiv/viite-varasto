import unittest
from config import app, db
# Ensure route decorators in src/app.py run and register endpoints
import app as app_module
from db_helper import setup_db, reset_db
from repositories.citation_repository import create_ref


class TestRefListModal(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()

    def tearDown(self):
        with app.app_context():
            reset_db()
            db.session.remove()

    def test_modal_and_info_button_present(self):
        with app.app_context():
            create_ref("article", "kw_modal", "Alice", "Modal Test", 2022)

        client = app.test_client()
        resp = client.get('/view_refs')
        self.assertEqual(resp.status_code, 200)
        text = resp.get_data(as_text=True)

        self.assertIn('id="refModal"', text)

        self.assertIn('class="info-btn"', text)
        self.assertIn('data-keyword="kw_modal"', text)

    def test_modal_shows_all_fields_in_markup(self):
        with app.app_context():
            create_ref("article", "kw2", "Bob", "Full Fields", 1999, journal="J Test", volume="1", pages="10-20", publisher="Pub", booktitle=None)

        client = app.test_client()
        resp = client.get('/view_refs')
        self.assertEqual(resp.status_code, 200)
        text = resp.get_data(as_text=True)

        self.assertIn('class="info-btn"', text)
        self.assertIn('data-journal=', text)
        self.assertIn('data-volume=', text)
        self.assertIn('data-pages=', text)
        self.assertIn('data-publisher=', text)


if __name__ == '__main__':
    unittest.main()
