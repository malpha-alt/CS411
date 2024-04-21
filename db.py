from flaskext.mysql import MySQL

mysql = MySQL()
app = None  # This will be set in the app initialization

def init_app(application):
    global app
    app = application
    mysql.init_app(app)

def get_db_connection():
    return mysql.connect()

def get_cursor():
    conn = get_db_connection()  
    return conn, conn.cursor()

def commit(conn):
    conn.commit()

def close_connection(conn):
    conn.close()