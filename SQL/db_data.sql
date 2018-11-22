TRUNCATE TABLE user;
INSERT INTO user (id, first_name, last_name, address, email, phone, admin, password) VALUES

(NULL, 'John', 'Doe', '125 Ave Du Parc', 'johndoe@gmail.com', '(514) 336-4545', 1, '$5$rounds=535000$Y9aJsj6nDUIxrdX8$KjzneFoNwSBd8MiedeoCuhDR3AnFTQeYm7vBrCV/9a4'),
(NULL, 'Jane', 'Dee', '125 Ave Du Parc', 'janedee@gmail.com', '(514) 336-4545', 1, '$5$rounds=535000$vaRcpprbw7lAYCxY$onE09j6O55tDz45aVn0IgzCe/pzwcp44Q1TdAnO6lmB'),
(NULL, 'Bob', 'Morane', '3000 Ganger ave', 'bob@gmail.com', '(514) 976-0327', 0, '$5$rounds=535000$hWigPp20nPqzUFTn$5wnADnsSsKFGYhcCFtyGh.sHXcNUmv.PrDKiFYQxll0'),
(NULL, 'Alice', 'Abernathy', '2002 Umbrella rd', 'alice@gmail.com', '(212) 767-2155', 1, '$5$rounds=535000$z4NOXYGdV2l5IUC0$2NkzDIhgIrZKYelebunTN0eubLqb02jXso/vgcx36u5'),
(NULL, 'Fred', 'Flintstone', '345 Cave Stone Road', 'fred@gmail.com', '(514) 123-4567', 0, '$5$rounds=535000$Y9aJsj6nDUIxrdX8$KjzneFoNwSBd8MiedeoCuhDR3AnFTQeYm7vBrCV/9a4');


TRUNCATE TABLE book;
INSERT INTO book (id, title, author, format, pages, publisher, publication_year, language, isbn10, isbn13, quantity) VALUES
(NULL, 'A Feast For Crows', 'George RR Martin', 'Hardcover', 250, 'Scholastic', 2005, 'English', 1234567890, 1234567890123, 2),
(NULL, 'Neuromancer', 'William Gibson', 'Paperback', 186, 'Random House', 1984, 'English', 1230987654, 1231234567890, 3),
(NULL, 'South of the Border', 'Haruki Murakami', 'Paperback', 213, 'Vintage International', 1998, 'English', 9780679767, 9780679767398, 2),
(NULL, 'The Prophet', 'Kahlil Gibran', 'Hardcover', 96, 'Alfred A. Knopf', 1923, 'English', 9781724757, 9781724757623, 1),
(NULL, 'Things Fall Apart', 'Chinua Achebe', 'Paperback', 209, 'Anchor Books', 1994, 'English', 3085474547, 3085474547123, 2),
(NULL, 'The Five People You Meet in Heaven', 'Mitch Albom', 'Paperback', 194, 'Hyperion', 2003, 'English', 9780786868, 9780786868711, 2);


TRUNCATE TABLE magazine;
INSERT INTO magazine (id, title, publisher, publication_date, language, isbn10, isbn13, quantity) VALUES
(NULL, 'The New York Times Magazine', 'Arthurr Ochs Sulzberger Jr.', '2018-11-23', 'English', 1439401890, 8461968342412, 2),
(NULL, 'National Geographic', 'Neil DeGrasse Tyson', '2013-06-17', 'English', 2234567890, 2234567890123, 3);

TRUNCATE TABLE movie;
INSERT INTO movie (id, title, director, producers, actors, language, subtitles, dubbed, release_date, runtime, quantity) VALUES
(NULL, 'The Last Jedi', 'Rian Johnson', 'Kathleen Kennedy', 'Mark Hamil, Carrie Fisher, Adam Driver and Daisy Ridley', 'English', 'None', 'None', '2017-12-15', '152 minutes', 2),
(NULL, 'One Flew over the Cuckoos Nest', 'Milos Forman', 'Lawrence Hauben', 'Jack Nicholson', 'English', 'None', 'None', '1975-11-19', '192 minutes', 3),
(NULL, 'Rushmore', 'Wes Anderson', 'Barry Mendel', 'Jason Schwartzman', 'English', 'English', 'None', '1998-12-11', '93 minutes', 1),
(NULL, 'Pulp Fiction', 'Quentin Tarantino', 'Lawrence Bender', 'John Travolta', 'English', 'English', 'French', '1994-10-14', '178 minutes', 2),
(NULL, 'Amadeus', 'Milos Forman', 'Saul Zaentz', 'F. Murray Abraham', 'English', 'French', 'None', '1984-09-06', '161 minutes', 1);

TRUNCATE TABLE music;
INSERT INTO music (id, title, media_type, artist, label, release_date, asin, quantity) VALUES
(NULL, 'Thriller', 'CD', 'Michael Jackson', 'Epic Records', '1982-11-30', 'B008FOB124', 2),
(NULL, 'The Path of Totality', 'CD', 'Korn', 'Roadrunner', '2011-06-12', 'B005V1WVPA', 2),
(NULL, 'The Dark Side of the Moon', 'CD', 'Pink Floyd', 'Harvest', '1973-03-01', 'B019VQSA64', 1),
(NULL, 'The Wall', 'CD', 'Pink Floyd', 'Harvest', '1979-11-30', 'B004ZN9W5M', 2),
(NULL, 'Rage Against The Machine', 'CD', 'Rage Against The Machine', 'Epic Records', '1992-11-03', 'B009A9EYUO', 2);


TRUNCATE TABLE book_physical;
INSERT INTO book_physical (id, item_fk, status, return_date) VALUES
(NULL, 1, "Available", NULL),
(NULL, 1, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 3, "Available", NULL),
(NULL, 3, "Available", NULL),
(NULL, 4, "Available", NULL),
(NULL, 5, "Available", NULL),
(NULL, 5, "Available", NULL),
(NULL, 6, "Available", NULL),
(NULL, 6, "Available", NULL);



TRUNCATE TABLE magazine_physical;
INSERT INTO magazine_physical (id, item_fk, status) VALUES
(NULL, 1, "Available"),
(NULL, 1, "Available"),
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
(NULL, 3, "Available", NULL),
(NULL, 4, "Available", NULL),
(NULL, 4, "Available",  NULL),
(NULL, 5, "Available",  NULL);


TRUNCATE TABLE music_physical;
INSERT INTO music_physical (id, item_fk, status, return_date) VALUES
(NULL, 1, "Available", NULL),
(NULL, 1, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 2, "Available", NULL),
(NULL, 3, "Available", NULL),
(NULL, 4, "Available", NULL),
(NULL, 4, "Available", NULL),
(NULL, 5, "Available", NULL),
(NULL, 5, "Available", NULL);
