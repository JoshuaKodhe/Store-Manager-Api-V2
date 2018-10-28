import unittest
from app.api.v1.models.user_model import User


class UserModelTest(unittest.TestCase):
    def setUp(self):
        self.new_user = User("test@gmail.com", "test")

    def test_init(self):
        '''
        test case to test if the object is initialized properly
        '''
        self.assertEqual(self.new_user.email, "test@gmail.com")
        self.assertEqual(self.new_user.password, "test")

    def test_save_user(self):
        '''
        test case to test if the user object is saved into the users_list
        '''
        self.new_user.save_user()
        self.assertEqual(len(User.users_list), 1)

    def test_fetch_user_by_email(self):
        '''
        test to check if we can find a user by phone email and display
        information
        '''
        self.new_user.save_user()
        test_user = User("new_test@gmail.com", "newtestpassword")  # new user
        test_user.save_user()

        found_user = User.fetch_single_user("new_test@gmail.com")
        self.assertEqual(found_user['email'], test_user.email)

    def tearDown(self):
        '''
        tearDown method that does clean up after each test case has run.
        '''
        User.users_list = []


if __name__ == '__main__':
    unittest.main()
