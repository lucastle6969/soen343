DROP TABLE IF EXISTS book;
CREATE TABLE book (
    id INT(20) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    status VARCHAR(20), 
    author VARCHAR(30), 
    format VARCHAR(20), 
    pages INT(255), 
    publisher VARCHAR(50), 
    language VARCHAR(30), 
    isbn10 BIGINT(10), 
    isbn13 BIGINT(13)
);


DROP TABLE IF EXISTS magazine;
CREATE TABLE magazine (
    id INT(20) AUTO_INCREMENT PRIMARY KEY, 
    title VARCHAR(100),
    status VARCHAR(20), 
    publisher VARCHAR(50), 
    language VARCHAR(30), 
    isbn10 BIGINT(10), 
    isbn13 BIGINT(13)
);


DROP TABLE IF EXISTS movie;
CREATE TABLE movie (
    id INT(20) AUTO_INCREMENT PRIMARY KEY, 
    title VARCHAR(100),
    status VARCHAR(20), 
    director VARCHAR(30), 
    producers VARCHAR(100), 
    actors VARCHAR(100), 
    language VARCHAR(30), 
    subtitles VARCHAR(30), 
    dubbed VARCHAR(30), 
    release_date VARCHAR(30), 
    runtime VARCHAR(20)
);


DROP TABLE IF EXISTS music;
CREATE TABLE music (
    id INT(20) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    status VARCHAR(20),
    media_type VARCHAR(30), 
    artist VARCHAR(30), 
    label VARCHAR(30),
    release_date VARCHAR(30), 
    asin VARCHAR(20)
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