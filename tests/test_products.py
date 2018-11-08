import unittest
from flask import json
from app import create_app
from .base_test import BaseTest, base_url


class TestProducts(BaseTest):
    def test_for_successful_product_registration(self):
        '''Tests for a successful product Addition'''
        product = json.dumps({"name": "chair",
                              "category": "furniture",
                              "price": 200,
                              "quantity": 15,
                              "description": "great for the back, must have"})

        resp = self.client.post(base_url+"/products",
                                data=product,
                                content_type='application/json')
        response = json.loads(resp.data)
        self.assertEqual(response["message"], "Successfully added")
        self.assertEqual(resp.status_code, 201)

    def test_post_product_empty_name(self):
        '''Tests for no product name'''
        invalid_product = json.dumps({"name": " ",
                                      "category": "furniture",
                                      "price": 200,
                                      "quantity": 15,
                                      "description": "great for the back, must have"})

        resp = self.client.post(base_url+"/products",
                                data=invalid_product,
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        self.assertEqual(data['message'],
                         "Ensure all the fields are correctly entered")
        self.assertEqual(resp.status_code, 400)

    def test_post_product_empty_price(self):
        '''Tests for no category'''
        invalid_product = json.dumps({"name": "chair",
                                      "category": " ",
                                      "price": 200,
                                      "quantity": 15,
                                      "description": "great for the back, must have"})

        resp = self.client.post(base_url+"/products",
                                data=invalid_product,
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        self.assertEqual(data['message'],
                         "Ensure all the fields are correctly entered")
        self.assertEqual(resp.status_code, 400)

    def test_post_product_extra_field(self):
        '''Tests for no price'''
        invalid_product = json.dumps({"name": "chair",
                                      "category": "furniture",
                                      "another": "another_one",
                                      "price": 200,
                                      "quantity": 15,
                                      "description": "great for the back, must have"})

        resp = self.client.post(base_url+"/products",
                                data=invalid_product,
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        self.assertEqual(data['message'],
                         "The field another is not a valid field")
        self.assertEqual(resp.status_code, 400)
