import unittest
from util import (
    validate_ref,
    validate_article_fields,
    validate_book_field,
    validate_inproceedings_field,
    UserInputError,
)


class TestRefValidation(unittest.TestCase):
    def test_valid_minimum_lengths_returns_parsed_year(self):
        self.assertEqual(validate_ref("article", "koodi", "titlee", "2020"), 2020)

    def test_valid_maximum_lengths_returns_parsed_year(self):
        self.assertEqual(validate_ref("book", "a" * 300, "b" * 300, 2025), 2025)

    def test_author_too_short_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("article", "ole", "validtitle", 2020)

    def test_title_too_long_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("article", "validauthor", "koodi" * 61, 2020)

    def test_invalid_ref_type_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("unknown", "validauthor", "validtitle", 2020)

    def test_non_integer_year_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("article", "validauthor", "validtitle", "notayear")

    def test_year_out_of_range_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("article", "validauthor", "validtitle", 9999)

    def test_none_author_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("article", None, "title", 2020)

    def test_none_title_raises(self):
        with self.assertRaises(UserInputError):
            validate_ref("article", "author", None, 2020)

    def test_valid_maximum_lengths_returns_parsed_year(self):
        self.assertEqual(validate_article_fields("j" * 300, "10", "p" * 300), 10)

    def test_journal_too_long_raises(self):
        with self.assertRaises(UserInputError):
            validate_article_fields("j" * 301, "10", "pages")

    def test_pages_too_long_raises(self):
        with self.assertRaises(UserInputError):
            validate_article_fields("journal", "10", "p" * 301)

    def test_publisher_too_long_raises(self):
        with self.assertRaises(UserInputError):
            validate_book_field("p" * 301)

    def test_booktitle_too_long_raises(self):
        with self.assertRaises(UserInputError):
            validate_inproceedings_field("b" * 301)


if __name__ == "__main__":
    unittest.main()
