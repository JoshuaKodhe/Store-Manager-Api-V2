from flask import json
from .base_test import BaseTest, base_url


class TestAuthentication(BaseTest):
    def test_registration(self):
        user = json.dumps({"email": "testuser@gmail.com",
                           "password": "asdfg",
                           "username": "testU"
                           })

        response = self.client.post(base_url+"/auth/register",
                                    data=user,
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "User testuser@gmail.com was created")
        self.assertEqual(response.status_code, 201)
