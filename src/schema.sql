CREATE TABLE citations (
  id SERIAL PRIMARY KEY, 
  type TEXT CHECK (type IN ('article', 'book', 'inproceedings', 'misc')) DEFAULT 'misc',
  author TEXT DEFAULT NULL,
  title TEXT DEFAULT NULL,
  year INT DEFAULT NULL
)