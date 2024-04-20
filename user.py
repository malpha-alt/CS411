from flask_login import UserMixin
import db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic

    @staticmethod
    def get(user_id):
        conn, cursor = db.get_cursor()
        try:
            cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if not user:
                return None
            user = User(
                id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
            )
            return user
        finally:
            cursor.close()
            db.close_connection(conn)

    @staticmethod
    def create(id_, name, email, profile_pic):
        conn, cursor = db.get_cursor()
        print("Creating user:", id_, name, email, profile_pic)
        try:
            cursor.execute("INSERT INTO user (id, name, email, profile_pic) VALUES (%s, %s, %s, %s)", (id_, name, email, profile_pic))
            db.commit(conn)
            print("Created user:", id_, name, email, profile_pic)
        except Exception as e:
            print("Failed to insert user:", e)
            raise
        finally:
            cursor.close()
            db.close_connection(conn)
