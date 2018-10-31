"""User class"""
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256


from app.utils.db_connection import init_db


class User:
    """User class defining methods related to the class"""
    def __init__(self, email, password):
        # add username
        self.email = email
        self.password = password
        self.registered_on = datetime.now()
        self.db = init_db()

    def save_user(self):
        """ save a new user """
        user = dict(email=self.email,
                    password=self.password,
                    registered_on=self.registered_on)

        cursor = self.db.cursor()

        cursor.execute(
            "INSERT INTO users (email,password,registered_on) \
               VALUES(%s,%s,%s)",
            (self.email, self.password, self.registered_on),)

        self.db.commit()
        self.db.close()
        return user

    def fetch_single_user(self, email):
        """Return a single user by email"""
        cursor = init_db().cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        user = cursor.fetchone()
        cursor.close()
        return user

    @staticmethod
    def check_if_user_exists(email):
        cursor = init_db().cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s;", (email,))
        result = cursor.fetchone()
        if result:
            return True
        return False

    @staticmethod
    def generate_hash(password):
        """Used to create a user encrypted password"""
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, pass_hash):
        """Used to check is two passwords match"""
        return sha256.verify(password, pass_hash)
