class UserInputError(Exception):
    pass

def validate_ref(ref_type, author, title, year):
    # Basic required-field checks
    if not ref_type:
        raise UserInputError("Reference type is required")

    if author is None or title is None:
        raise UserInputError("Author and title are required")

    # Normalize strings
    author = str(author).strip()
    title = str(title).strip()

    # Length limits (match form: min 5, max 300)
    MIN_LEN = 5
    MAX_LEN = 300
    MAX_YEAR = 2026

    if len(author) < MIN_LEN or len(title) < MIN_LEN:
        raise UserInputError(f"Author and title must be at least {MIN_LEN} characters long")

    if len(author) > MAX_LEN or len(title) > MAX_LEN:
        raise UserInputError(f"Author and title must be at most {MAX_LEN} characters long")

    # Reference type validation
    allowed_types = ['article', 'book', 'inproceedings', 'misc']
    if ref_type not in allowed_types:
        raise UserInputError("Invalid reference type")

    # Year: convert to int and validate range
    try:
        year_int = int(year)
    except (TypeError, ValueError):
        raise UserInputError("Year must be an integer")

    if year_int < 1 or year_int > MAX_YEAR:
        raise UserInputError("Invalid year")

    # Return parsed year for convenience to callers
    return year_int
