from flask import json
from .base_test import BaseTest, base_url


class TestAuthLogin(BaseTest):
    def test_user_login(self):
        """Test for weather you can login with correct credentials"""
        self.register()

        response = self.client.post(base_url+'/auth/login',
                                    data=self.user_login,
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data["message"], 'Logged in as testuser@gmail.com')
        self.assertEqual(response.status_code, 200)

    def test_empty_email_login(self):
        """Test for when user logins without email"""
        response = self.client.post(base_url+'/auth/login',
                                    data=self.empty_email_login,
                                    content_type='application/json')
        data = json.loads(response.data.decode())

        self.assertEqual(data['message'], "Enter email and password to login")
        self.assertEqual(response.status_code, 400)

    def test_empty_password_login(self):
        """Test for when user does not enter a password"""
        response = self.client.post(base_url+'/auth/login',
                                    data=self.empty_pass_login,
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], "Enter email and password to login")
        self.assertEqual(response.status_code, 400)

    def test_wrong_email_login(self):
        """Test for when user enters wrong email"""
        self.register()

        response = self.client.post(base_url+'/auth/login',
                                    data=self.wrong_email_login,
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], "User does not exist")
        self.assertEqual(response.status_code, 404)

    def test_wrong_password_login(self):
        """Test for when user enters wrong password"""
        self.register()

        response = self.client.post(base_url+'/auth/login',
                                    data=self.wrong_pass_login,
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], "Invalid password")
        self.assertEqual(response.status_code, 400)
