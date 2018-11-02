"""User class"""
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256


from app.utils.db_connection import connect


class User:
    """User class defining methods related to the class"""
    def __init__(self, email, username, password, role='attendant'):
        # add username
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.registered_on = datetime.now()

    def save_user(self):
        """ save a new user """
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO users (email,username,\
                                                   password,role,\
                                                   registered_on)\
                                VALUES(%s,%s,%s,%s,%s) \
                                RETURNING username", (self.email,
                                                      self.username,
                                                      self.password,
                                                      self.role,
                                                      self.registered_on))
                user = cursor.fetchone()
                return dict(username=user)

    @classmethod
    def fetch_single_user(cls, email):
        """Return a single user by email"""
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s;",
                               (email,))
                user = cursor.fetchone()
                print(user)
                return dict(email=user[1], username=user[2],
                            password=user[3], role=user[4])

    @staticmethod
    def check_if_user_exists(email):
        """Method to check if the user is in the system"""
        with connect() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s;",
                               (email,))
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
