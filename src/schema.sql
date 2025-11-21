CREATE TABLE citations (
  id SERIAL PRIMARY KEY, 
  keyword TEXT NOT NULL,
  type TEXT CHECK (type IN ('article', 'book', 'inproceedings', 'misc')) DEFAULT 'misc' NOT NULL,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  year INT NOT NULL
)