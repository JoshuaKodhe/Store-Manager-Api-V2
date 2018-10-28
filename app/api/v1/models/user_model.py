"""User class"""
from passlib.hash import pbkdf2_sha256 as sha256


class User:
    """User class defining methods related to the class"""
    users_list = []

    def __init__(self, email, password):
        self.user_id = len(self.users_list)+1
        self.email = email
        self.password = password

    def save_user(self):
        """ save a new user """
        user = dict(user_id=self.user_id,
                    email=self.email,
                    password=self.password)

        User.users_list.append(user)
        return user

    @classmethod
    def fetch_single_user(cls, email):
        """ Method to get a user"""
        for user in User.users_list:
            if user['email'] == email:
                return user
        return False

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, pass_hash):
        return sha256.verify(password, pass_hash)
