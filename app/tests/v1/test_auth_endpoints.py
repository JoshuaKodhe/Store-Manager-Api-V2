import unittest
from flask import json
from app import create_app

REGISTER_URL = '/api/v1/auth/register'
LOGIN_URL = '/api/v1/auth/login'


class TestAuthEndPoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.valid_register_user = {"email": "testuser@gmail.com",
                                    "password": "asdfg",
                                    "username": "testU"
                                    }
        self.blank_email = {"email": "",
                            "password": "asdfg",
                            "username": "testU"
                            }
        self.blank_password = {"email": "testuser@gmail.com",
                               "password": "",
                               "username": "testU"
                               }
        self.login_user = {"email": "testuser@gmail.com",
                           "password": "asdfg",
                           }
        self.wrong_email_login = {"email": "none@gmail.com",
                                  "password": "asdfg",
                                  }
        self.wrong_password_login = {"email": "testuser@gmail.com",
                                     "password": "fdsa",
                                     }

    def test_registration(self):
        response = self.client.post(REGISTER_URL,
                                    data=json.dumps(self.valid_register_user),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "User testuser@gmail.com was created")
        self.assertEqual(response.status_code, 201)

    def test_empty_email_register(self):
        response = self.client.post(REGISTER_URL,
                                    data=json.dumps(self.blank_email),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "Please enter a valid email")
        self.assertEqual(response.status_code, 400)

    def test_empty_password_register(self):
        response = self.client.post(REGISTER_URL,
                                    data=json.dumps(self.blank_password),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_user_login(self):
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(self.login_user),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data["access_token"])
        self.assertEqual(response.status_code, 200)

    def test_empty_email_login(self):
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(self.blank_email),
                                    content_type='application/json')
        data = json.loads(response.data.decode())

        self.assertEqual(data['message'], "The field username is not a valid field")
        self.assertEqual(response.status_code, 400)

    def test_empty_password_login(self):
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(self.blank_password),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], "The field username is not a valid field")
        self.assertEqual(response.status_code, 400)

    def test_wrong_email_login(self):
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(self.wrong_email_login),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], "User does not exist")
        self.assertEqual(response.status_code, 404)

    def test_wrong_password_login(self):
        response = self.client.post(LOGIN_URL,
                                    data=json.dumps(self.wrong_password_login),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'], "Invalid password")
        self.assertEqual(response.status_code, 400)
