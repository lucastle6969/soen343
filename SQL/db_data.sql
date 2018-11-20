TRUNCATE TABLE user;
INSERT INTO user (id, first_name, last_name, address, email, phone, admin, password) VALUES

(NULL, 'John', 'Doe', '125 Ave Du Parc', 'johndoe@gmail.com', '514-336-4545', 1, '$5$rounds=535000$Y9aJsj6nDUIxrdX8$KjzneFoNwSBd8MiedeoCuhDR3AnFTQeYm7vBrCV/9a4'),
(NULL, 'Jane', 'Dee', '125 Ave Du Parc', 'janedee@gmail.com', '514-336-4545', 1, '$5$rounds=535000$vaRcpprbw7lAYCxY$onE09j6O55tDz45aVn0IgzCe/pzwcp44Q1TdAnO6lmB'),
(NULL, 'Bob', 'Morane', '3000 Ganger ave', 'bob@gmail.com', '(514) 976-0327', 0, '$5$rounds=535000$hWigPp20nPqzUFTn$5wnADnsSsKFGYhcCFtyGh.sHXcNUmv.PrDKiFYQxll0'),
(NULL, 'Alice', 'Abernathy', '2002 Umbrella rd', 'alice@gmail.com', '(212) 767-2155', 1, '$5$rounds=535000$z4NOXYGdV2l5IUC0$2NkzDIhgIrZKYelebunTN0eubLqb02jXso/vgcx36u5'),
(NULL, 'Fred', 'Flintstone', '345 Cave Stone Road', 'fred@gmail.com', '(514) 123-4567', 0, '$5$rounds=535000$Y9aJsj6nDUIxrdX8$KjzneFoNwSBd8MiedeoCuhDR3AnFTQeYm7vBrCV/9a4');


TRUNCATE TABLE book;
INSERT INTO book (id, title, author, format, pages, publisher, publication_year, language, isbn10, isbn13, quantity) VALUES
(NULL, 'A Feast For Crows', 'George RR Martin', 'Hardcover', 250, 'Scholastic', 2005, 'English', 1234567890, 1234567890123, 2),
(NULL, 'Neuromancer', 'William Gibson', 'Paperback', 186, 'Random House', 1984, 'English', 1230987654, 1231234567890, 10);

TRUNCATE TABLE magazine;
INSERT INTO magazine (id, title, publisher, publication_date, language, isbn10, isbn13, quantity) VALUES
(NULL, 'The New York Times Magazine', 'Arthurr Ochs Sulzberger Jr.', '2018-11-23', 'English', 1439401890, 8461968342412, 2),
(NULL, 'National Geographic', 'Neil DeGrasse Tyson', '2013-06-17', 'English', 2234567890, 2234567890123, 10);

TRUNCATE TABLE movie;
INSERT INTO movie (id, title, director, producers, actors, language, subtitles, dubbed, release_date, runtime, quantity) VALUES
(NULL, 'The Last Jedi', 'Rian Johnson', 'Kathleen Kennedy', 'Mark Hamil, Carrie Fisher, Adam Driver and Daisy Ridley', 'English', 'None', 'None', '2017-12-15', '152 minutes', 2),
(NULL, 'One Flew over the Cuckoos Nest', 'Milos Forman', 'Lawrence Hauben', 'Jack Nicholson', 'English', 'None', 'None', '1975-11-19', '192 minutes', 10);

TRUNCATE TABLE music;
INSERT INTO music (id, title, media_type, artist, label, release_date, asin, quantity) VALUES
(NULL, 'Thriller', 'CD', 'Michael Jackson', 'Epic Records', '1982-11-30', 'B008FOB124', 2),
(NULL, 'The Path of Totality', 'CD', 'Korn', 'Roadrunner', '2011-06-12', 'Q1W2E3R4T5', 10);


TRUNCATE TABLE book_physical;
INSERT INTO book_physical (id, item_fk, status, return_date) VALUES
(NULL, 1, "Available", NULL),
(NULL, 1, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL);


TRUNCATE TABLE magazine_physical;
INSERT INTO magazine_physical (id, item_fk, status) VALUES
(NULL, 1, "Available"),
(NULL, 1, "Available"),
(NULL, 2, "Available"),
(NULL, 2, "Available"),
(NULL, 2, "Available"),
(NULL, 2, "Available"),
(NULL, 2, "Available"),
(NULL, 2, "Available"),
(NULL, 2, "Available"),
(NULL, 2, "Available"),
(NULL, 2, "Available"),
(NULL, 2, "Available");


TRUNCATE TABLE movie_physical;
INSERT INTO movie_physical (id, item_fk, status, return_date) VALUES
(NULL, 1, "Available", NULL),
(NULL, 1, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL);


TRUNCATE TABLE music_physical;
INSERT INTO music_physical (id, item_fk, status, return_date) VALUES
(NULL, 1, "Available", NULL),
(NULL, 1, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL),
(NULL, 2, "Available",  NULL);