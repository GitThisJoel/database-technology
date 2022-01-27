DROP TABLE IF EXISTS authors;
CREATE TABLE authors (
  author_ssn     TEXT,
  name           TEXT,
  PRIMARY KEY    (author_ssn)
);

DROP TABLE IF EXISTS books;
CREATE TABLE books (
  isbn          TEXT,
  title         TEXT,
  PRIMARY KEY   (isbn)
);

DROP TABLE IF EXISTS authorships;
CREATE TABLE authorships (
  isbn          TEXT,
  author_ssn    TEXT,
  FOREIGN KEY (isbn) REFERENCES books(isbn),
  FOREIGN KEY (author_ssn) REFERENCES authors(author_ssn),
  PRIMARY KEY (isbn, author_ssn)
);


-- example guardian
DROP TABLE IF EXISTS borrowers;
CREATE TABLE borrowers (
  ssn           TEXT
  -- ...
  PRIMARY KEY   (ssn)
  FOREIGN KEY (guardian_ssn) REFERENCES borrowers(ssn),
);
