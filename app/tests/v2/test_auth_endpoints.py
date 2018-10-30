import unittest
from flask import json
from app import create_app
from app.db_setup import DB

register_api = "/api/v2/auth/register"


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='testing')
        self.db = DB("testing")
        self.db.create_tables()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        '''Method to clear all tables
        before another test is undertaken'''
        self.db.destroy_tables()
        self.app_context.pop()

    def test_registration(self):
        user = json.dumps({"email": "testuser@gmail.com",
                           "password": "asdfg",
                           "username": "testU"
                           })

        response = self.client.post(register_api,
                                    data=user,
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "User testuser@gmail.com was created")
        self.assertEqual(response.status_code, 201)
