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
        i = 0
        for row in cur.fetchall():
            data.append(row)
            i += 1
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
        return new_magazine_id

    def add_movie(self, movie):
        return new_movie_id

    def add_music(self, music):
        return new_music_id

    def get_books(self):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM book")
        data = []
        i = 0
        for row in cur.fetchall():
            data.append(row)
            i += 1
        cur.close()
        if result is None:
            return False
        else:
            return data

    def get_movies(self):
        return None

    def get_magazines(self):
        return None

    def get_music(self):
        return None
