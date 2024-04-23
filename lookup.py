import db

def getEmailFromId(id):
    conn, cursor = db.get_cursor()
    cursor.execute(
        "SELECT email FROM User WHERE id = '{0}'".format(id))
    return cursor.fetchone()[0]

def getUserIdFromEmail(email):
    conn, cursor = db.get_cursor()
    cursor.execute(
        "SELECT id FROM User WHERE email = '{0}'".format(email))
    return cursor.fetchone()[0]

def isEmailUnique(email):
    # use this to check if a email has already been registered
    conn, cursor = db.get_cursor()
    if cursor.execute("SELECT email FROM User WHERE email = '{0}'".format(email)):
        # this means there are greater than zero entries with that email
        cursor.close()
        conn.close()
        return False
    else:
        cursor.close()
        conn.close()
        return True
  
def getFirstNameFromId(id):
    conn, cursor = db.get_cursor()
    cursor.execute(
        "SELECT name  FROM User WHERE id = '{0}'".format(id))
    return cursor.fetchone()[0]