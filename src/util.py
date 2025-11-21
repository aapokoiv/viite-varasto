class UserInputError(Exception):
    pass

def validate_ref(ref_type, keyword, author, title, year):
    if not ref_type:
        raise UserInputError("Reference type is required")

    if author is None or title is None or year is None or keyword is None:
        raise UserInputError("Author, title, year and keyword are required")

    author = str(author).strip()
    title = str(title).strip()

    MIN_LEN = 3

    if len(author) < MIN_LEN or len(title) < MIN_LEN:
        raise UserInputError(f"Author and title must be at least {MIN_LEN} characters long")

    allowed_types = ['article', 'book', 'inproceedings', 'misc']
    if ref_type not in allowed_types:
        raise UserInputError("Invalid reference type")

    try:
        year_int = int(year)
    except (TypeError, ValueError):
        raise UserInputError("Year must be an integer")

    return year_int
