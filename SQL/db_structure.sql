DROP TABLE IF EXISTS book;
CREATE TABLE book (
    id INT(20) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(30), 
    format VARCHAR(20), 
    pages INT(255), 
    publisher VARCHAR(50), 
    language VARCHAR(30), 
    isbn10 BIGINT(10), 
    isbn13 BIGINT(13),
    quantity tinyint(3)
);

DROP TABLE IF EXISTS book_physical;
CREATE TABLE book_physical (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    book_fk int(11),
    status VARCHAR(100)
);


DROP TABLE IF EXISTS magazine;
CREATE TABLE magazine (
    id INT(20) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    publisher VARCHAR(50), 
    language VARCHAR(30), 
    isbn10 BIGINT(10), 
    isbn13 BIGINT(13),
    quantity tinyint(3)
);

DROP TABLE IF EXISTS magazine_physical;
CREATE TABLE magazine_physical (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    magazine_fk int(11),
    status VARCHAR(100)
);


DROP TABLE IF EXISTS movie;
CREATE TABLE movie (
    id INT(20) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    director VARCHAR(30), 
    producers VARCHAR(100), 
    actors VARCHAR(100), 
    language VARCHAR(30), 
    subtitles VARCHAR(30), 
    dubbed VARCHAR(30), 
    release_date VARCHAR(30), 
    runtime VARCHAR(20),
    quantity tinyint(3)
);

DROP TABLE IF EXISTS movie_physical;
CREATE TABLE movie_physical (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    movie_fk int(11),
    status VARCHAR(100)
);



DROP TABLE IF EXISTS music;
CREATE TABLE music (
    id INT(20) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    media_type VARCHAR(30), 
    artist VARCHAR(30), 
    label VARCHAR(30),
    release_date VARCHAR(30), 
    asin VARCHAR(20),
    quantity tinyint(3)
);

DROP TABLE IF EXISTS music_physical;
CREATE TABLE music_physical (
    id INT(11) AUTO_INCREMENT PRIMARY KEY,
    music_fk int(11),
    status VARCHAR(100)
);


DROP TABLE IF EXISTS user;
CREATE TABLE user(
    id INT(20) AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50), 
    last_name VARCHAR(50), 
    address VARCHAR(50), 
    email VARCHAR(50), 
    phone VARCHAR(60), 
    admin tinyint(1), 
    password VARCHAR(100)
);