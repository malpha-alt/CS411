from flask_login import UserMixin
import db
import uuid

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, password_hash):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.password_hash =password_hash

    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(user_id):
        conn, cursor = db.get_cursor()
        try:
            cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return None
            user = User(
                id_=user[0], name=user[1], email=user[2], profile_pic=user[3], password_hash=user[4]
            )
            return user
        finally:
            cursor.close()
            db.close_connection(conn)

    @staticmethod
    def create(id_, name, email, profile_pic, password_hash):
        conn, cursor = db.get_cursor()
        print("Creating user:", id_, name, email, profile_pic, password_hash)
        try:
            cursor.execute("INSERT INTO user (id, name, email, profile_pic, password_hash) VALUES (%s, %s, %s, %s, %s)", (id_, name, email, profile_pic, password_hash))
            db.commit(conn)
            print("Created user:", id_, name, email, profile_pic, password_hash)
        except Exception as e:
            print("Failed to insert user:", e)
            raise
        finally:
            cursor.close()
            db.close_connection(conn)

    @staticmethod
    def create_user(name, email, hashed_password):
        conn, cursor = db.get_cursor()
        try:
            cursor.execute("INSERT INTO User (id, name, email, password_hash, profile_pic) VALUES (%s, %s, %s, %s, %s)", (str(uuid.uuid4()), name, email, hashed_password, None))
            db.commit(conn)
            return True
        except Exception as e:
            print(e)  # Log the error for debugging
            return False
        finally:
            db.close_connection(conn)