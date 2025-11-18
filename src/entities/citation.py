class Citation:
    def __init__(self, id, keyword, type, author, title, year):
        self.id = id
        self.keyword = keyword
        self.type = type
        self.author = author
        self.title = title
        self.year = year

    def __str__(self):
        return f"{self.title}"
