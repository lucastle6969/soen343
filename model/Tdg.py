from flaskext.mysql import MySQL
from dpcontracts import require

class UserTdg:
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

    def modify_user(self, user_id, first_name, last_name, address, email, phone):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("UPDATE user SET first_name = %s, last_name = %s, address = %s, email = %s, phone = %s WHERE id = %s",
                    (first_name, last_name, address, email, phone, user_id))
        cur.close()

    def modify_password(self, user_id, password):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("UPDATE user SET password = %s WHERE id = %s", (password, user_id))
        cur.close()

    def delete_user(self, user_id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("DELETE FROM user WHERE id = %s", user_id)
        cur.close()

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

    def get_user_by_id(self, id):
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

    def get_all_users_active_loans(self):
        # This query gets all users and all the loans of those users.
        connection = self.mysql.connect()
        cur = connection.cursor()
        sql = "SELECT u.id, u.first_name, u.last_name, u.address, u.email, u.phone, u.admin, u.password, bp.id, bp.item_fk, bp.status, bp.return_date, bp.user_fk, mup.id, mup.item_fk, mup.status, mup.return_date, mup.user_fk, mop.id, mop.item_fk, mop.status, mop.return_date, mop.user_fk "
        sql += "FROM user AS u LEFT JOIN book_physical AS bp ON (u.id = bp.user_fk) "
        sql += "LEFT JOIN music_physical AS mup ON (u.id = mup.user_fk) "
        sql += "LEFT JOIN movie_physical AS mop ON (u.id = mop.user_fk) WHERE 1 "
        result = cur.execute(sql)
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def get_logs(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, user_fk, log_type, timestamp FROM historical_user_log_registry")
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def add_log(self, user_id, log_type, timestamp):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("""INSERT INTO historical_user_log_registry(user_fk, log_type, timestamp) VALUES(%s, %s, %s)""", (user_id, log_type, timestamp))
        result = cur.execute("SELECT * FROM log_registry ORDER BY timestamp DESC")
        if result > 0:
            last_historical_id = cur.fetchone()
            last_historical_id = last_historical_id[0]
        else:
            last_historical_id = False
        cur.close()
        return last_historical_id


class ItemTdg:
    def __init__(self, app):
        self.mysql = MySQL()

        # Config MySQL
        app.config['MYSQL_DATABASE_USER'] = 'pomoroad_soen09'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'discordApp343'
        app.config['MYSQL_DATABASE_DB'] = 'pomoroad_soen343'
        app.config['MYSQL_DATABASE_HOST'] = '108.167.160.63'

        # init MYSQL
        self.mysql.init_app(app)

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

    def add_book(self, book):
        connection = self.mysql.connect()
        cur = connection.cursor()
        # Execute query
        cur.execute("""INSERT INTO book(title, author, format, pages, publisher, publication_year, language, isbn10, isbn13, quantity)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (book.title, book.author, book.format, book.pages, book.publisher, book.publication_year, book.language, book.isbn10, book.isbn13, book.quantity))
        # get the new user id
        result = cur.execute("SELECT * FROM book ORDER BY id DESC LIMIT 1")
        new_book_id = cur.fetchone()
        self.add_physical_book(book.quantity, new_book_id, cur)
        # send new id back to the controller
        cur.close()
        if result > 0:
            return new_book_id[0]
        else:
            new_book_id = False
        return new_book_id

    def add_physical_book(self, quantity, id, cur):
        for x in range(0, quantity):
            cur.execute("""INSERT INTO book_physical(item_fk, status) VALUES (%s, %s)""", (str(id[0]), "Available"))

    def add_magazine(self, magazine):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("""INSERT INTO magazine(title, publisher, publication_date, language, isbn10, isbn13, quantity)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                    (magazine.title, magazine.publisher, magazine.publication_date, magazine.language, magazine.isbn10, magazine.isbn13, magazine.quantity))
        result = cur.execute("SELECT * FROM magazine ORDER BY id DESC LIMIT 1")
        new_magazine_id = cur.fetchone()
        self.add_physical_magazine(magazine.quantity, new_magazine_id, cur)
        cur.close()
        if result > 0:
            return new_magazine_id[0]
        else:
            new_magazine_id = False
        return new_magazine_id

    def add_physical_magazine(self, quantity, id, cur):
        for x in range(0, quantity):
            cur.execute("""INSERT INTO magazine_physical(item_fk, status) VALUES (%s, %s)""", (str(id[0]), "Available"))

    def add_movie(self, movie):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("""INSERT INTO movie(title, director, producers, actors, language, subtitles, dubbed, release_date, runtime, quantity)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (movie.title, movie.director, movie.producers, movie.actors, movie.language, movie.subtitles, movie.dubbed, movie.release_date, movie.runtime, movie.quantity))
        result = cur.execute("SELECT * FROM movie ORDER BY id DESC LIMIT 1")
        new_movie_id = cur.fetchone()
        self.add_physical_movie(movie.quantity, new_movie_id, cur)
        cur.close()
        if result > 0:
            return new_movie_id[0]
        else:
            new_movie_id = False
        return new_movie_id

    def add_physical_movie(self, quantity, id, cur):
        for x in range(0, quantity):
            cur.execute("""INSERT INTO movie_physical(item_fk, status) VALUES (%s, %s)""", (str(id[0]), "Available"))

    def add_music(self, music):
        connection = self.mysql.connect()
        cur = connection.cursor()
        cur.execute("""INSERT INTO music(title, media_type, artist, label, release_date, asin, quantity)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)""",
                    (music.title, music.media_type, music.artist, music.label, music.release_date, music.asin, music.quantity))
        result = cur.execute("SELECT * FROM music ORDER BY id DESC LIMIT 1")
        new_music_id = cur.fetchone()
        self.add_physical_music(music.quantity, new_music_id, cur)
        cur.close()
        if result > 0:
            return new_music_id[0]
        else:
            new_music_id = False
        return new_music_id

    def add_physical_music(self, quantity, id, cur):
        for x in range(0, quantity):
            cur.execute("""INSERT INTO music_physical(item_fk, status) VALUES (%s, %s)""", (str(id[0]), "Available"))

    def get_books(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, title, author, format, pages, publisher, publication_year, language, isbn10, isbn13, quantity FROM book WHERE 1")
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def get_books_physical(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, item_fk, status, return_date, user_fk FROM book_physical")
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
        result = cur.execute("SELECT id, title, publisher, publication_date, language, isbn10, isbn13, quantity FROM magazine WHERE 1")
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def get_magazines_physical(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, item_fk, status FROM magazine_physical")
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

    def get_movies_physical(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, item_fk, status, return_date, user_fk FROM movie_physical")
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

    def get_music_physical(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, item_fk, status, return_date, user_fk FROM music_physical")
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
            cur.execute("DELETE FROM book_physical WHERE item_fk = %s", book.id)
        # ideally a check if there were errors here and return a boolean to be handled by the mapper
        cur.close()

    def delete_magazines(self, deleted_magazines):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for magazine in deleted_magazines:
            cur.execute("DELETE FROM magazine WHERE id = %s", magazine.id)
            cur.execute("DELETE FROM magazine_physical WHERE item_fk = %s", magazine.id)
        cur.close()

    def delete_movies(self, deleted_movies):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for movie in deleted_movies:
            cur.execute("DELETE FROM movie WHERE id = %s", movie.id)
            cur.execute("DELETE FROM movie_physical WHERE item_fk = %s", movie.id)
        cur.close()

    def delete_music(self, deleted_music):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for music in deleted_music:
            cur.execute("DELETE FROM music WHERE id = %s", music.id)
            cur.execute("DELETE FROM music_physical WHERE item_fk = %s", music.id)
        cur.close()

    def modify_books(self, modified_books):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for book in modified_books:
            cur.execute("UPDATE book SET title = %s, author = %s, format = %s, pages = %s, publisher = %s, publication_year = %s, language = %s, isbn10 = %s, isbn13 = %s , quantity = %s WHERE id = %s", (book.title, book.author, book.format, book.pages, book.publisher, book.publication_year, book.language, book.isbn10, book.isbn13, book.quantity, book.id))
        cur.close()

    def modify_physical_book(self, id, added_amount, removed_item):
        connection = self.mysql.connect()
        cur = connection.cursor()
        added_item_ids = []
        if len(added_amount) != 0:
            for x in added_amount:
                if x[0] == "bb" and id == int(x[2]):
                    for y in range(0, int(x[1])):
                        cur.execute("""INSERT INTO book_physical(item_fk, status) VALUES (%s, %s)""", (str(id), "Available"))
                        added_item_ids.append(int(cur.execute("""SELECT LAST_INSERT_ID()""")))
        if len(removed_item) != 0:
            for (prefix,  book_id) in removed_item:
                if prefix == "bb" and int(book_id) == id:
                    for item_id in removed_item[(prefix, book_id)]:
                        cur.execute("DELETE FROM book_physical WHERE id = %s", (int(item_id)))
        cur.close()
        return added_item_ids

    def modify_magazines(self, modified_magazines):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for magazine in modified_magazines:
            cur.execute("UPDATE magazine SET title = %s, publisher = %s, publication_date = %s, language = %s, isbn10 = %s, isbn13 = %s, quantity = %s WHERE id = %s", (magazine.title, magazine.publisher, magazine.publication_date, magazine.language, magazine.isbn10, magazine.isbn13, magazine.quantity, magazine.id))
        cur.close()

    def modify_physical_magazine(self, id, added_amount, removed_item):
        connection = self.mysql.connect()
        cur = connection.cursor()
        added_item_ids = []
        if len(added_amount) != 0:
            for x in added_amount:
                if x[0] == "ma" and id == int(x[2]):
                    for y in range(0, int(x[1])):
                        cur.execute("""INSERT INTO magazine_physical(item_fk, status) VALUES (%s, %s)""", (str(id), "Available"))
                        added_item_ids.append(int(cur.execute("""SELECT LAST_INSERT_ID()""")))
        if len(removed_item) != 0:
            for (prefix,  magazine_id) in removed_item:
                if prefix == "ma" and int(magazine_id) == id:
                    for item_id in removed_item[(prefix, magazine_id)]:
                        cur.execute("DELETE FROM magazine_physical WHERE id = %s", (int(item_id)))
        cur.close()
        return added_item_ids

    def modify_movies(self, modified_movies):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for movie in modified_movies:
            cur.execute("UPDATE movie SET title = %s, director = %s, producers = %s, actors = %s, language = %s, subtitles = %s, dubbed = %s, release_date = %s, runtime = %s, quantity = %s WHERE id = %s", (movie.title, movie.director, movie.producers, movie.actors, movie.language, movie.subtitles, movie.dubbed, movie.release_date, movie.runtime, movie.quantity, movie.id))
        cur.close()

    def modify_physical_movie(self, id, added_amount, removed_item):
        connection = self.mysql.connect()
        cur = connection.cursor()
        added_item_ids = []
        if len(added_amount) != 0:
            for x in added_amount:
                if x[0] == "mo" and id == int(x[2]):
                    for y in range(0, int(x[1])):
                        cur.execute("""INSERT INTO movie_physical(item_fk, status) VALUES (%s, %s)""", (str(id), "Available"))
                        added_item_ids.append(int(cur.execute("""SELECT LAST_INSERT_ID()""")))
        if len(removed_item) != 0:
            for (prefix,  movie_id) in removed_item:
                if prefix == "mo" and int(movie_id) == id:
                    for item_id in removed_item[(prefix, movie_id)]:
                        cur.execute("DELETE FROM movie_physical WHERE id = %s", (int(item_id)))
        cur.close()
        return added_item_ids

    def modify_music(self, modified_music):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for music in modified_music:
            cur.execute("UPDATE music SET title = %s, media_type = %s, artist = %s, label = %s, release_date = %s, asin = %s, quantity = %s WHERE id = %s", (music.title, music.media_type, music.artist, music.label, music.release_date, music.asin, music.quantity, music.id))
        cur.close()

    def modify_physical_music(self, id, added_amount, removed_item):
        connection = self.mysql.connect()
        cur = connection.cursor()
        added_item_ids = []
        if len(added_amount) != 0:
            for x in added_amount:
                if x[0] == "mu" and id == int(x[2]):
                    for y in range(0, int(x[1])):
                        cur.execute("""INSERT INTO music_physical(item_fk, status) VALUES (%s, %s)""", (str(id), "Available"))
                        added_item_ids.append(int(cur.execute("""SELECT LAST_INSERT_ID()""")))
        if len(removed_item) != 0:
            for (prefix,  music_id) in removed_item:
                if prefix == "mu" and int(music_id) == id:
                    for item_id in removed_item[(prefix, music_id)]:
                        cur.execute("DELETE FROM music_physical WHERE id = %s", (int(item_id)))
        cur.close()
        return added_item_ids

    def get_physical_keys(self, id, prefix):
        connection = self.mysql.connect()
        cur = connection.cursor()
        keys = []
        if prefix == "bb":
            result = cur.execute("SELECT id FROM book_physical WHERE item_fk = "+str(id))
        if prefix == "ma":
            result = cur.execute("SELECT id FROM magazine_physical WHERE item_fk = "+str(id))
        if prefix == "mo":
            result = cur.execute("SELECT id FROM movie_physical WHERE item_fk = "+str(id))
        if prefix == "mu":
            result = cur.execute("SELECT id FROM music_physical WHERE item_fk = "+str(id))
        for row in cur.fetchall():
            keys.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return keys

    def mark_as_returned(self, physical_items):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for item in physical_items:
            if item.prefix == "bb":
                cur.execute("UPDATE book_physical SET status = 'Available', user_fk = NULL, return_date = NULL WHERE id = %s", item.id)
            elif item.prefix == "mo":
                cur.execute("UPDATE movie_physical SET status = 'Available', user_fk = NULL, return_date = NULL WHERE id = %s", item.id)
            elif item.prefix == "mu":
                cur.execute("UPDATE music_physical SET status = 'Available', user_fk = NULL, return_date = NULL WHERE id = %s", item.id)
        cur.close()
        return True

    @require("All passed items must be available to loan", lambda args: (args.self.catalog.get_physical_items_from_tuple(item.prefix, item_fk, item.id).status == 'Available' for item in args.loaned_items))
    def loan_items(self, loaned_items):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for item in loaned_items:
            if item.prefix == "bb":
                cur.execute("UPDATE book_physical SET status = 'Loaned', user_fk = %s, return_date = %s WHERE id = %s", (item.user_fk, item.return_date, item.id))
            elif item.prefix == "mo":
                cur.execute("UPDATE movie_physical SET status = 'Loaned', user_fk = %s, return_date = %s WHERE id = %s", (item.user_fk, item.return_date, item.id))
            elif item.prefix == "mu":
                cur.execute("UPDATE music_physical SET status = 'Loaned', user_fk = %s, return_date = %s WHERE id = %s", (item.user_fk, item.return_date, item.id))
        cur.close()
        return True


class TransactionTdg:
    def __init__(self, app):
        self.mysql = MySQL()

        # Config MySQL
        app.config['MYSQL_DATABASE_USER'] = 'pomoroad_soen09'
        app.config['MYSQL_DATABASE_PASSWORD'] = 'discordApp343'
        app.config['MYSQL_DATABASE_DB'] = 'pomoroad_soen343'
        app.config['MYSQL_DATABASE_HOST'] = '108.167.160.63'

        # init MYSQL
        self.mysql.init_app(app)

    def get_transactions(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, user_fk, prefix, item_fk, physical_id, transaction_type, timestamp FROM transaction_registry WHERE 1")
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def get_active_loans(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT id, user_fk, prefix, item_fk, physical_id, return_date FROM active_loan_registry WHERE 1")
        data = []
        for row in cur.fetchall():
            data.append(row)
        cur.close()
        if result is None:
            return False
        else:
            return data

    def add_transactions(self, user_id, physical_items, transaction_type, timestamp):
        connection = self.mysql.connect()
        cur = connection.cursor()
        for item in physical_items:
            cur.execute("""INSERT INTO transaction_registry(user_fk, prefix, item_fk, physical_id, transaction_type, timestamp)
                    VALUES(%s, %s, %s, %s, %s, %s)""", (user_id, item.prefix, item.item_fk, item.id, transaction_type, timestamp))
            if transaction_type is "loan":
                cur.execute("""INSERT INTO active_loan_registry(user_fk, prefix, item_fk, physical_id, return_date)
                    VALUES(%s, %s, %s, %s, %s)""", (user_id, item.prefix, item.item_fk, item.id, item.return_date))
            elif transaction_type is "return":
                cur.execute("DELETE FROM active_loan_registry WHERE user_fk = %s AND prefix = %s AND physical_id = %s", (user_id, item.prefix, item.id))

        result = cur.execute("SELECT * FROM transaction_registry ORDER BY id DESC LIMIT 1")
        if result > 0:
            last_historical_id = cur.fetchone()
            last_historical_id = last_historical_id[0]
        else:
            last_historical_id = None
        if transaction_type is "loan":
            result = cur.execute("SELECT * FROM active_loan_registry ORDER BY id DESC LIMIT 1")
            if result > 0:
                last_active_id = cur.fetchone()
                last_active_id = last_active_id[0]
            else:
                last_active_id = None
        else:
            last_active_id = None
        last_ids = []
        last_ids.append(last_historical_id)
        last_ids.append(last_active_id)
        cur.close()
        return last_ids
