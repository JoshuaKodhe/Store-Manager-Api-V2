import unittest
from flask import json
from app import create_app
from .base_test import BaseTest, base_url


class TestProducts(BaseTest):
    def test_for_successful_product_registration(self):
        '''Tests for a successful product Addition'''
        response = self.client.post(base_url+"/products",
                                    data=self.poper_product,
                                    headers=dict(Authorization="Bearer "+self.login()),
                                    content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(data["message"], "Successfully added")
        self.assertEqual(response.status_code, 201)

    def test_post_product_empty_name(self):
        '''Tests for no product name'''
        response = self.client.post(base_url+"/products",
                                    data=self.no_product_name,
                                    headers=dict(Authorization="Bearer "+self.login()),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "Ensure all the fields are correctly entered")
        self.assertEqual(response.status_code, 400)

    def test_post_product_empty_price(self):
        '''Tests for no category'''
        response = self.client.post(base_url+"/products",
                                    data=self.no_product_name,
                                    headers=dict(Authorization="Bearer "+self.login()),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "Ensure all the fields are correctly entered")
        self.assertEqual(response.status_code, 400)

    def test_post_product_extra_field(self):
        '''Tests for no price'''

        response = self.client.post(base_url+"/products",
                                    data=self.no_product_price,
                                    headers=dict(Authorization="Bearer "+self.login()),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "The field another is not a valid field")
        self.assertEqual(response.status_code, 400)
