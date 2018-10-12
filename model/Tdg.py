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
    def insertUser(self, firstName, lastName, address, email, phone, admin, password):
        connection = self.mysql.connect()
        cur = connection.cursor()
         # Execute query
        cur.execute("INSERT INTO clientAdmin(id, firstName, lastName, physicalAddress, email, phone, admin, password) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s)", (firstName, lastName, address, email, phone, admin, password))
        # Close connection
        cur.close()

    # -- SELECT Queries
    def getUserByEmail(self, email):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM clientAdmin WHERE email = %s", [email])
        data = cur.fetchone()
        #send data back to the controller
        if result > 0:
            return data
        else:
            data = False
        cur.close()
        return data

    def getItemById(self, id):
        connection = self.mysql.connect()
        cur = connection.cursor()
        result = cur.execute("SELECT * FROM clientAdmin WHERE id = %s", [id])
        data = cur.fetchone()
        cur.close()
        if result is None:
            return False
        else:
            return data
