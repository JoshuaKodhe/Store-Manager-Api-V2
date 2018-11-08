from flask import json
from .base_test import BaseTest, base_url


class TestSale(BaseTest):
    def test_get_sales(self):
        '''Tests for a successful product Addition'''
        response = self.client.get(base_url+"/sales",
                                   headers=dict(Authorization="Bearer "+self.login()),
                                   content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(data["message"], "retrieved successfully")
        self.assertEqual(response.status_code, 200)

    def test_get_sale(self):
        '''Tests for a successful product Addition'''

        response = self.client.get(base_url+"/sales",
                                   data=self.poper_product,
                                   headers=dict(Authorization="Bearer "+self.login()),
                                   content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(data["message"], "retrieved successfully")
        self.assertEqual(response.status_code, 200)
