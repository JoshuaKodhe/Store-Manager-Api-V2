import unittest
from flask import json
from app import create_app
from app.db_setup import DB

product_url = "/api/v2/products"


class TestProducts(unittest.TestCase):
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

    def test_for_successful_product_registration(self):
        '''Tests for a successful product Addition'''
        product = json.dumps({"name": "chair",
                              "category": "furniture",
                              "price": 200,
                              "quantity": 15,
                              "description": "great for the back, must have"})

        resp = self.client.post(product_url,
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

        resp = self.client.post(product_url,
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

        resp = self.client.post(product_url,
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

        resp = self.client.post(product_url,
                                data=invalid_product,
                                content_type='application/json')
        data = json.loads(resp.data.decode())
        self.assertEqual(data['message'],
                         "The field another is not a valid field")
        self.assertEqual(resp.status_code, 400)
