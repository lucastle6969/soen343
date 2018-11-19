INSERT INTO book_physical (item_fk, status, return_date, user_fk)
VALUES (2, "Loaned", (DATE_ADD(now() , INTERVAL 7 DAY)), 3);
INSERT INTO book_physical (item_fk, status, return_date, user_fk)
VALUES (1, "Loaned", (DATE_ADD(now() , INTERVAL 5 DAY)), 3);
INSERT INTO movie_physical (item_fk, status, return_date, user_fk)
VALUES (2, "Loaned", (DATE_ADD(now() , INTERVAL 2 DAY)), 3);
INSERT INTO movie_physical (item_fk, status, return_date, user_fk)
VALUES (1, "Loaned", (DATE_ADD(now() , INTERVAL 1 DAY)), 3);
INSERT INTO music_physical (item_fk, status, return_date, user_fk)
VALUES (2, "Loaned", (DATE_ADD(now() , INTERVAL 2 DAY)), 3);
INSERT INTO music_physical (item_fk, status, return_date, user_fk)
VALUES (1, "Loaned", (DATE_ADD(now() , INTERVAL 1 DAY)), 3);