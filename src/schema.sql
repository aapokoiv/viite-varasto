CREATE TABLE citations (
  id SERIAL PRIMARY KEY, 
  type TEXT CHECK (type IN ('article', 'book', 'inproceedings', 'misc')) DEFAULT 'misc',
  author TEXT DEFAULT NULL,
  title TEXT DEFAULT NULL,
  year INT DEFAULT NULL,
  booktitle TEXT DEFAULT NULL,
  journal TEXT DEFAULT NULL,
  volume INT DEFAULT NULL,
  pages TEXT DEFAULT NULL,
  publisher TEXT DEFAULT NULL
)