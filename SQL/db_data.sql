TRUNCATE TABLE user;
INSERT INTO user VALUES (1, 'John', 'Doe', '125 Ave Du Parc', 'johndoe@gmail.com', '514-336-4545', 1, '$5$rounds=535000$Y9aJsj6nDUIxrdX8$KjzneFoNwSBd8MiedeoCuhDR3AnFTQeYm7vBrCV/9a4');
INSERT INTO user VALUES (2, 'John', 'Doe', '125 Ave Du Parc', 'a', '514-336-4545', 1, '$5$rounds=535000$vaRcpprbw7lAYCxY$onE09j6O55tDz45aVn0IgzCe/pzwcp44Q1TdAnO6lmB');

TRUNCATE TABLE book;
INSERT INTO book VALUES (NULL, 'A Feast For Crows', 'George RR Martin', 'Physical', 250, 'Scholastic', 'English', 1234567890, 1234567890123, 2);
INSERT INTO book VALUES (NULL, 'Neuromancer', 'William Gibson', 'Paperback', 186, 'Random House', 'English', 1230987654, 1231234567890, 1);

TRUNCATE TABLE magazine;
INSERT INTO magazine VALUES (NULL, 'The New York Times Magazine', 'Arthurr Ochs Sulzberger Jr.', 'English', 1439401890, 8461968342412, 2);
INSERT INTO magazine VALUES (NULL, 'National Geographic', 'Neil DeGrasse Tyson', 'English', 1234567890, 1234567890123, 1);

TRUNCATE TABLE movie;
INSERT INTO movie VALUES (NULL, 'The Last Jedi', 'Rian Johnson', 'Kathleen Kennedy', 'Mark Hamil, Carrie Fisher, Adam Driver and Daisy Ridley', 'English', 'None', 'None', 'Dec. 15 2017', '152 minutes', 2);
INSERT INTO movie VALUES (NULL, 'One Flew over the Cuckoos Nest', 'Milos Forman', 'Lawrence Hauben', 'Jack Nicholson', 'English', 'None', 'None', 'Nov. 19, 1975', '192 minutes', 1);

TRUNCATE TABLE music;
INSERT INTO music VALUES (NULL, 'Thriller', 'CD', 'Michael Jackson', 'Epic Records', 'Nov. 30 1982', 'B008FOB124', 2);
INSERT INTO music VALUES (NULL, 'The Path of Totality', 'CD', 'Korn', 'Roadrunner', 'Dec. 6 2011', 'Q1W2E3R4T5', 1);


TRUNCATE TABLE book_physical;
INSERT INTO book_physical VALUES (NULL, 1, "Available");
INSERT INTO book_physical VALUES (NULL, 1, "Loaned");
INSERT INTO book_physical VALUES (NULL, 2, "Available");


TRUNCATE TABLE magazine_physical;
INSERT INTO magazine_physical VALUES (NULL, 1, "Available");
INSERT INTO magazine_physical VALUES (NULL, 1, "Loaned");
INSERT INTO magazine_physical VALUES (NULL, 2, "Available");


TRUNCATE TABLE movie_physical;
INSERT INTO movie_physical VALUES (NULL, 1, "Available");
INSERT INTO movie_physical VALUES (NULL, 1, "Loaned");
INSERT INTO movie_physical VALUES (NULL, 2, "Available");


TRUNCATE TABLE music_physical;
INSERT INTO music_physical VALUES (NULL, 1, "Available");
INSERT INTO music_physical VALUES (NULL, 1, "Loaned");
INSERT INTO music_physical VALUES (NULL, 2, "Available");