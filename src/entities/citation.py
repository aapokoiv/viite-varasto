class Citation:
    def __init__(self, id, keyword, type, author, title, year, doi, category, booktitle=None, journal=None, volume=None, pages=None, publisher=None):  # pylint: disable=redefined-builtin
        self.id = id
        self.keyword = keyword
        self.type = type
        self.author = author
        self.title = title
        self.year = year
        self.doi = doi
        self.category = category
        self.booktitle = booktitle
        self.journal = journal
        self.volume = volume
        self.pages = pages
        self.publisher = publisher

    def __str__(self):
        return f"{self.title}"
