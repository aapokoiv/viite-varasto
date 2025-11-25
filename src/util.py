class UserInputError(Exception):
    pass

def validate_ref(ref_type, keyword, author, title, year):
    if not ref_type:
        raise UserInputError("Reference type is required")

    if author is None or title is None or year is None or keyword is None:
        raise UserInputError("Author, title, year and keyword are required")

    author = str(author).strip()
    title = str(title).strip()

    min_len = 3

    if len(author) < min_len or len(title) < min_len:
        raise UserInputError(f"Author and title must be at least {min_len} characters long")

    allowed_types = ['article', 'book', 'inproceedings', 'misc']
    if ref_type not in allowed_types:
        raise UserInputError("Invalid reference type")

    try:
        year_int = int(year)
    except (TypeError, ValueError):
        raise UserInputError("Year must be an integer") from None

    return year_int

def validate_article_fields(journal, volume, pages):    # pylint: disable=unused-argument
    if volume:
        try:
            volume = int(volume)
        except (TypeError, ValueError):
            raise UserInputError("Volume must be an integer") from None
    return volume
