from flaskext.mysql import MySQL


class Tdg:
    def __init__(self, app):
        self.mysql = MySQL()

        # Config MySQL
        app.config['MYSQL_DATABASE_USER'] = 'pomoroad_soen09'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'discordApp343'
        app.config['MYSQL_DATABASE_DB'] = 'pomoroad_soen343'
        app.config['MYSQL_DATABASE_HOST'] = '108.167.160.63'

        # init MYSQL
        self.mysql.init_app(app)

    # User SQL Queries

    # -- INSERT Queries
    def insert_user(self, first_name, last_name, address, email, phone, admin, password):
        connection = self.mysql.connect()
        cur = connection.cursor()
        # Execute query
        cur.execute("""INSERT INTO user(id, first_name, last_name, address, email, phone, admin, password)
                    VALUES(NULL, %s, %s, %s, %s, %s, %s, %s)""",
                    (first_name, last_name, address, email, phone, admin, password))
        # get the new user id
        result = cur.execute("SELECT * FROM user WHERE email = %s", [email])
        new_user_id = cur.fetchone()
        cur.close()
        # send data back to the controller
        if result > 0:
            return new_user_id[0]
        else:
            new_user_id = False
        return new_user_id

    # -- SELECT Queries
    def get_user_by_email(self, email):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM user WHERE email = %s", [email])
        data = cur.fetchone()
        cur.close()
        # send data back to the controller
        if result > 0:
            return data
        else:
            data = False

        return data

    def get_item_by_id(self, id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM user WHERE id = %s", [id])
        data = cur.fetchone()
        cur.close()
        if result is None:
            return False
        else:
            return data

    def get_all_users(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM user WHERE 1")
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def add_book(self, book):
        connection = self.mysql.connect()
        cur = connection.cursor()
        # Execute query
        cur.execute("""INSERT INTO book(title, author, format, pages, publisher, language, isbn10, isbn13, quantity)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (book.title, book.author, book.format, book.pages, book.publisher, book.language, book.isbn10, book.isbn13, book.quantity))
        # get the new user id
        result = cur.execute("SELECT * FROM book ORDER BY id DESC LIMIT 1")
        new_book_id = cur.fetchone()
        for x in range(0, book.quantity):
            cur.execute("""INSERT INTO book_physical(book_fk, status) VALUES (%s, %s)""", (str(new_book_id[0]), "Available"))
        # send new id back to the controller
        cur.close()
        if result > 0:
            return new_book_id[0]
        else:
            new_book_id = False
        return new_book_id

    def add_magazine(self, magazine):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("""INSERT INTO magazine(title, publisher, language, isbn10, isbn13, quantity)
                    VALUES(%s, %s, %s, %s, %s, %s)""",
                    (magazine.title, magazine.publisher, magazine.language, magazine.isbn10, magazine.isbn13, magazine.quantity))
        result = cur.execute("SELECT * FROM magazine ORDER BY id DESC LIMIT 1")
        new_magazine_id = cur.fetchone()
        for x in range(0, magazine.quantity):
            cur.execute("""INSERT INTO magazine_physical(magazine_fk, status) VALUES (%s, %s)""", (str(new_magazine_id[0]), "Available"))
        cur.close()
        if result > 0:
            return new_magazine_id[0]
        else:
            new_magazine_id = False
        return new_magazine_id

    def add_movie(self, movie):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("""INSERT INTO movie(title, director, producers, actors, language, subtitles, dubbed, release_date, runtime, quantity)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (movie.title, movie.director, movie.producers, movie.actors, movie.language, movie.subtitles, movie.dubbed, movie.release_date, movie.runtime, movie.quantity))
        result = cur.execute("SELECT * FROM movie ORDER BY id DESC LIMIT 1")
        new_movie_id = cur.fetchone()
        for x in range(0, movie.quantity):
            cur.execute("""INSERT INTO movie_physical(movie_fk, status) VALUES (%s, %s)""", (str(new_movie_id[0]), "Available"))
        cur.close()
        if result > 0:
            return new_movie_id[0]
        else:
            new_movie_id = False
        return new_movie_id

    def add_music(self, music):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("""INSERT INTO music(title, media_type, artist, label, release_date, asin, quantity)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                    (music.title, music.media_type, music.artist, music.label, music.release_date, music.asin, music.quantity))
        result = cur.execute("SELECT * FROM music ORDER BY id DESC LIMIT 1")
        new_music_id = cur.fetchone()
        for x in range(0, music.quantity):
            cur.execute("""INSERT INTO music_physical(music_fk, status) VALUES (%s, %s)""", (str(new_music_id[0]), "Available"))
        cur.close()
        if result > 0:
            return new_music_id[0]
        else:
            new_music_id = False
        return new_music_id

    def get_books(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, title, author, format, pages, publisher, language, isbn10, isbn13, quantity FROM book WHERE 1")
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def get_magazines(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, title, publisher, language, isbn10, isbn13, quantity FROM magazine WHERE 1")
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def get_movies(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, title, director, producers, actors, language, subtitles, dubbed, release_date, runtime, quantity FROM movie WHERE 1")
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def get_music(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, title, media_type, artist, label, release_date, asin, quantity FROM music WHERE 1")
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def delete_books(self, deleted_books):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for book in deleted_books:
            cur.execute("DELETE FROM book WHERE id = %s", book.id)
        # ideally a check if there were errors here and return a boolean to be handled by the mapper
        cur.close()

    def delete_magazines(self, deleted_magazines):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for magazine in deleted_magazines:
            cur.execute("DELETE FROM magazine WHERE id = %s", magazine.id)
        cur.close()

    def delete_movies(self, deleted_movies):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for movie in deleted_movies:
            cur.execute("DELETE FROM movie WHERE id = %s", movie.id)
        cur.close()

    def delete_music(self, deleted_music):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for music in deleted_music:
            cur.execute("DELETE FROM music WHERE id = %s", music.id)
        cur.close()

    def modify_books(self, modified_books):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for book in modified_books:
            cur.execute("UPDATE book SET title = %s, author = %s, format = %s, pages = %s, publisher = %s, language = %s, isbn10 = %s, isbn13 = %s WHERE id = %s", (book.title, book.author, book.format, book.pages, book.publisher, book.language, book.isbn10, book.isbn13, book.id))
        # ideally a check if there were errors here and return a boolean to be handled by the mapper
        cur.close()

    def modify_magazines(self, modified_magazines):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for magazine in modified_magazines:
            cur.execute("UPDATE magazine SET title = %s, publisher = %s, language = %s, isbn10 = %s, isbn13 = %s WHERE id = %s", (magazine.title, magazine.publisher, magazine.language, magazine.isbn10, magazine.isbn13, magazine.id))
        cur.close()

    def modify_movies(self, modified_movies):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for movie in modified_movies:
            cur.execute("UPDATE movie SET title = %s, director = %s, producers = %s, actors = %s, language = %s, subtitles = %s, dubbed = %s, release_date = %s, runtime = %s WHERE id = %s", (movie.title, movie.director, movie.producers, movie.actors, movie.language, movie.subtitles, movie.dubbed, movie.release_date, movie.runtime, movie.id))
        cur.close()

    def modify_music(self, modified_music):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for music in modified_music:
            cur.execute("UPDATE music SET title = %s, media_type = %s, artist = %s, label = %s, release_date = %s, asin = %s WHERE id = %s", (music.title, music.media_type, music.artist, music.label, music.release_date, music.asin, music.id))
        cur.close()

    # [Testing] Used to verify add/remove/modify test objects
    def get_last_inserted_id(self, table_name):
        connection = self.mysql.connect()
        cur = connection.cursor()

        result = cur.execute("SELECT * FROM " + table_name + " ORDER BY id DESC LIMIT 1")
        item_id = cur.fetchone()
        cur.close()

        if result > 0:
            return item_id[0]
        else:
            item_id = False
        return item_id
