DROP TABLE IF EXISTS theaters;

CREATE TABLE theaters(
  name      TEXT,
  capacity	INT,
  PRIMARY KEY (name)
);

DROP TABLE IF EXISTS screenings;

CREATE TABLE screenings(
  screening_id TEXT DEFAULT (lower(hex(randomblob(16)))),
  start_time   TIME,
  start_date   DATE,
  t_name	   TEXT,
  m_title	   TEXT,
  m_year	   INT,

  FOREIGN KEY (t_name) REFERENCES theaters(name)
  FOREIGN KEY (m_title, m_year) REFERENCES movies(title, year)
  PRIMARY KEY (screening_id)
);

DROP TABLE IF EXISTS movies;

CREATE TABLE movies(
  title        TEXT,
  year		   INT,
  imdb_key	   TEXT,
  running_time INT,
  PRIMARY KEY (title, year)
);

DROP TABLE IF EXISTS customers;

CREATE TABLE customers(
  username      TEXT,
  password    	TEXT,
  first_name	TEXT,
  last_name		TEXT,
  PRIMARY KEY (username)
);

DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
  ticket_id	      TEXT DEFAULT (lower(hex(randomblob(16)))),
  screening_id	  TEXT,
  customer_uname  TEXT,
  FOREIGN KEY (screening_id)   REFERENCES screenings(screening_id),
  FOREIGN KEY (customer_uname) REFERENCES customers(username),
  PRIMARY KEY (ticket_id)
);

INSERT INTO movies (title, year, imdb_key, running_time)
VALUES ('Taxi' ,       1998, 'tt0152930', 86),
	   ('Taxi 2',      2000, 'tt0183869', 88),
	   ('Taxi 3',      2004, 'tt0295721', 84),
	   ('Taxi 4',      2007, 'tt0804540', 91),
	   ('Taxi 5',      2018, 'tt7238392', 102),
	   ('Taxi Driver', 1976, 'tt0075314', 114);

INSERT INTO theaters (name, capacity)
VALUES ('Bio Roy 1', 150),
	   ('Filmstaden Lund 1', 800);


INSERT INTO screenings (t_name, m_title, m_year, start_date, start_time)
VALUES ('Bio Roy 1',         'Taxi',        1998, '2022-03-25', '19:30'),
	   ('Filmstaden Lund 1', 'Taxi Driver', 1976, '2022-09-27', '22:00'),
	   ('Bio Roy 1',         'Taxi 3',      2004, '2022-09-08', '13:37'),
	   ('Filmstaden Lund 1', 'Taxi 5', 		2018, '2022-04-20', '04:20');
	   
INSERT INTO customers (username, password, first_name, last_name)
VALUES ('PhantomBomb', '409', 'Fredrik', 'Voigt'),
	   ('GitThisJoel', '418', 'Joel', 'Bäcker'),
	   ('Deysteria99', '404', 'Axel', 'Svensson');
