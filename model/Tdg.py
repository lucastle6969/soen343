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
        cur.execute("""INSERT INTO clientAdmin(id, firstName, lastName, physicalAddress, email, phone, admin, password)
                    VALUES(NULL, %s, %s, %s, %s, %s, %s, %s)""",
                    (first_name, last_name, address, email, phone, admin, password))
        # get the new user id
        result = cur.execute("SELECT * FROM clientAdmin WHERE email = %s", [email])
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
        result = cur.execute("SELECT * FROM clientAdmin WHERE email = %s", [email])
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
        result = cur.execute("SELECT * FROM clientAdmin WHERE id = %s", [id])
        data = cur.fetchone()
        cur.close()
        if result is None:
            return False
        else:
            return data

    def get_all_users(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM clientAdmin WHERE 1")
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
        cur.execute("""INSERT INTO book(title, author, format, pages, publisher, language, isbn10, isbn13)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (book.title, book.author, book.format, book.pages, book.publisher, book.language, book.isbn10, book.isbn13))
        # get the new user id
        result = cur.execute("SELECT * FROM book ORDER BY id DESC LIMIT 1")
        new_book_id = cur.fetchone()
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
        cur.execute("""INSERT INTO magazine(title, publisher, language, isbn10, isbn13)
                    VALUES(%s, %s, %s, %s, %s)""",
                    (magazine.title, magazine.publisher, magazine.language, magazine.isbn10, magazine.isbn13))
        result = cur.execute("SELECT * FROM magazine ORDER BY id DESC LIMIT 1")
        new_magazine_id = cur.fetchone()
        cur.close()
        if result > 0:
            return new_magazine_id[0]
        else:
            new_magazine_id = False
        return new_magazine_id

    def add_movie(self, movie):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("""INSERT INTO movie(title, director, producers, actors, language, subs, dubbed, release_date, runtime)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (movie.title, movie.director, movie.producers, movie.actors, movie.language, movie.subs, movie.dubbed, movie.release_date, movie.runtime))
        result = cur.execute("SELECT * FROM movie ORDER BY id DESC LIMIT 1")
        new_movie_id = cur.fetchone()
        cur.close()
        if result > 0:
            return new_movie_id[0]
        else:
            new_movie_id = False
        return new_movie_id

    def add_music(self, music):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("""INSERT INTO music(title, media_type, artist, label, release_date, asin)
                    VALUES(%s, %s, %s, %s, %s, %s)""",
                    (music.title, music.media_type, music.artist, music.label, music.release_date, music.asin))
        result = cur.execute("SELECT * FROM music ORDER BY id DESC LIMIT 1")
        new_music_id = cur.fetchone()
        cur.close()
        if result > 0:
            return new_music_id[0]
        else:
            new_music_id = False
        return new_music_id

    def get_books(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM book WHERE 1")
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
        result = cur.execute("SELECT * FROM magazine WHERE 1")
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
        result = cur.execute("SELECT * FROM movie WHERE 1")
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
        result = cur.execute("SELECT * FROM music WHERE 1")
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
        # Delete first item (index 0) in the array from the database
        cur.execute("DELETE * FROM book WHERE id = %s", (deleted_books[0].id))
        # Remove first item from the array
        deleted_books.pop(0)
        # Tentative for/while loop to continuously remove first item from the database and then the array
        """for row in deleted_books:
            OR while deleted_books[0] is not None:
            cur.execute("DELETE * FROM book WHERE id = %s", (row.id))
            deleted_books.pop(0)"""
        cur.close()
        # Return updated array to controller (either with one less item or completely empty)
        return deleted_books

    def delete_magazines(self, deleted_magazines):
        pass

    def delete_movies(self, deleted_movies):
        pass

    def delete_music(self, deleted_music):
        pass

    def modify_books(self, modified_books):
        connection = self.mysql.connect()
        cur = connection.cursor()
        # Update all columns for a specified item (the first in the array)
        cur.execute("UPDATE book SET title = %s, author = %s, format = %s, pages = %s, publisher = %s, language = %s, isbn10 = %s, isbn13 = %s WHERE id = %s",
                    (modified_books[0].title, modified_books[0].author, modified_books[0].format, modified_books[0].publisher, modified_books[0].language, modified_books[0].isbn10, modified_books[0].isbn13, modified_books[0].id))
        # Remove first item from the array
        modified_books.pop(0)
        # Tentative for/while loop to continuously update first item from the database and then remove from the array
        """for row in modified_books:
            OR while modified_books[0] is not None:
            cur.execute("UPDATE book SET title = %s, author = %s, format = %s, pages = %s, publisher = %s, language = %s, isbn10 = %s, isbn13 = %s WHERE id = %s",
                        (modified_books[0].title, modified_books[0].author, modified_books[0].format, modified_books[0].publisher, modified_books[0].language, modified_books[0].isbn10, modified_books[0].isbn13, modified_books[0].id))
            modified_books.pop(0)"""
        cur.close()
        # Return updated array to controller (either with one less item or completely empty)
        return modified_books

    def modify_magazines(self, modified_magazines):
        pass

    def modify_movies(self, modified_movies):
        pass

    def modify_music(self, modified_music):
        pass
