import unittest

from util import UserInputError, validate_article_fields, validate_ref


class TestRefValidation(unittest.TestCase):
    def test_valid_add_returns_parsed_year(self):
        self.assertEqual(validate_ref("article", "kw", "koodi", "titlee", "2020"), 2020)

    def test_missing_ref_type_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref(None, "kw", "author", "title", 2020)

    def test_missing_keyword_author_title_or_year_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("article", None, "author", "title", 2020)

        with self.assertRaises(UserInputError):
            validate_ref("article", "kw", None, "title", 2020)

        with self.assertRaises(UserInputError):
            validate_ref("article", "kw", "author", None, 2020)

        with self.assertRaises(UserInputError):
            validate_ref("article", "kw", "author", "title", None)

    def test_author_or_title_too_short_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("article", "kw", "ab", "validtitle", 2020)

        with self.assertRaises(UserInputError):
            validate_ref("article", "kw", "validauthor", "ab", 2020)

    def test_invalid_ref_type_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("unknown", "kw", "validauthor", "validtitle", 2020)

    def test_non_integer_year_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("article", "kw", "validauthor", "validtitle", "notanint")

    def test_validate_article_returns_parsed_volume(self):
        self.assertEqual(validate_article_fields("journal", "10", "pages"), 10)


if __name__ == "__main__":
    unittest.main()
