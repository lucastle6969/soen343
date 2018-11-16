DROP TABLE IF EXISTS book;
CREATE TABLE book (
    id INT(6) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(30), 
    format VARCHAR(20), 
    pages INT(255), 
    publisher VARCHAR(50), 
    publication_year INT(4),
    language VARCHAR(30), 
    isbn10 BIGINT(10), 
    isbn13 BIGINT(13),
    quantity TINYINT(3)
);

DROP TABLE IF EXISTS book_physical;
CREATE TABLE book_physical (
    id INT(6) AUTO_INCREMENT PRIMARY KEY,
    item_fk INT(6),
    status VARCHAR(100),
    return_date DATETIME,
    user_fk INT(6) NULL DEFAULT NULL
);


DROP TABLE IF EXISTS magazine;
CREATE TABLE magazine (
    id INT(6) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    publisher VARCHAR(50),
    publication_date VARCHAR(30), 
    language VARCHAR(30), 
    isbn10 BIGINT(10), 
    isbn13 BIGINT(13),
    quantity TINYINT(3)
);

DROP TABLE IF EXISTS magazine_physical;
CREATE TABLE magazine_physical (
    id INT(6) AUTO_INCREMENT PRIMARY KEY,
    item_fk INT(6),
    status VARCHAR(100)
);


DROP TABLE IF EXISTS movie;
CREATE TABLE movie (
    id INT(6) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    director VARCHAR(30), 
    producers VARCHAR(100), 
    actors VARCHAR(100), 
    language VARCHAR(30), 
    subtitles VARCHAR(30), 
    dubbed VARCHAR(30), 
    release_date VARCHAR(30), 
    runtime VARCHAR(20),
    quantity TINYINT(3)
);

DROP TABLE IF EXISTS movie_physical;
CREATE TABLE movie_physical (
    id INT(6) AUTO_INCREMENT PRIMARY KEY,
    item_fk INT(6),
    status VARCHAR(100),
    return_date DATETIME,
    user_fk INT(6) NULL DEFAULT NULL
);



DROP TABLE IF EXISTS music;
CREATE TABLE music (
    id INT(6) AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100),
    media_type VARCHAR(30), 
    artist VARCHAR(30), 
    label VARCHAR(30),
    release_date VARCHAR(30), 
    asin VARCHAR(20),
    quantity TINYINT(3)
);

DROP TABLE IF EXISTS music_physical;
CREATE TABLE music_physical (
    id INT(6) AUTO_INCREMENT PRIMARY KEY,
    item_fk INT(6),
    status VARCHAR(100),
    return_date DATETIME,
    user_fk INT(6) NULL DEFAULT NULL
);


DROP TABLE IF EXISTS user;
CREATE TABLE user(
    id INT(7) AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50), 
    last_name VARCHAR(50), 
    address VARCHAR(50), 
    email VARCHAR(50), 
    phone VARCHAR(60), 
    admin TINYINT(1), 
    password VARCHAR(100)
);

DROP TABLE IF EXISTS transaction_registry;
CREATE TABLE transaction_registry(
    id INT(20) AUTO_INCREMENT PRIMARY KEY,
    user_fk INT(7),
    prefix VARCHAR(2),
    physical_id INT(6),
    transaction_type VARCHAR(6),
    timestamp DATETIME
);

DROP TABLE IF EXISTS active_loan_registry;
CREATE TABLE active_loan_registry(
    id INT(10) AUTO_INCREMENT PRIMARY KEY,
    user_fk INT(7),
    prefix VARCHAR(2),
    physical_id INT(6),
    return_date DATETIME  
);

DROP TABLE IF EXISTS cart;
CREATE TABLE cart(
    id INT(7) AUTO_INCREMENT PRIMARY KEY,
    user_fk INT(7),
    prefix VARCHAR(2),
    physical_id_fk INT(6)
);
