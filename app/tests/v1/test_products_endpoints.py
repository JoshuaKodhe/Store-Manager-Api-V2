import unittest
from flask import json
from app import create_app
from app.api.v1.models.products_model import Product

BASE_URL = '/api/v1/products'
SINGLE_PROD_URL = '/api/v1/products/{}'
LOGIN_URL = '/api/v1/auth/login'


class TestProductsEndpoint(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.product_item = {"name": "Table",
                             "description": "The product description here",
                             "quantity": 12,
                             "category": "Furniture",
                             "unit price": 2000}

        self.empty_product_name_item = {"name": "",
                                        "description": "The product description here",
                                        "quantity": 12,
                                        "category": "Furniture",
                                        "unit price": 2000}
        self.empty_product_description_item = {"name": "Chair ",
                                               "description": " ",
                                               "quantity": 12,
                                               "category": "Furniture",
                                               "unit price": 2000}
        self.empty_product_quantity_item = {"name": "Chair",
                                            "description": "The product description here",
                                            "category": "Furniture",
                                            "unit price": 2000,
                                            "quantity": ""}
        self.empty_product_price_item = {"name": "Chair",
                                         "description": "The product description here",
                                         "category": "Furniture",
                                         "unit price": "",
                                         "quantity": 12}

        self.empty_product_category_item = {"name": "Chair",
                                            "description": "The product description here",
                                            "category": "",
                                            "unit price": 2000,
                                            "quantity": 12}

        self.login_user = {"email": "testuser@gmail.com",
                           "password": "asdfg",
                           }

    def login(self):
        response = self.client().post(LOGIN_URL,
                                      data=json.dumps(self.login_user),
                                      content_type='application/json')
        access_token = json.loads(response.get_data())["access_token"]
        return access_token

    def test_post_product(self):
        """ Test for posting a single product """
        response = self.client().post(BASE_URL,
                                      data=json.dumps(self.product_item),
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_post_product_empty_name(self):
        """ Test for posting a single product """
        response = self.client().post(BASE_URL,
                                      data=json.dumps(self.empty_product_name_item),
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "Ensure all the fields are correctly entered")
        self.assertEqual(response.status_code, 400)

    def test_post_product_empty_description(self):
        """ Test for posting a single product """
        response = self.client().post(BASE_URL,
                                      data=json.dumps(self.empty_product_description_item),
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "Ensure all the fields are correctly entered")
        self.assertEqual(response.status_code, 400)

    def test_post_product_empty_quantity(self):
        """ Test for posting a single product """
        response = self.client().post(BASE_URL,
                                      data=json.dumps(self.empty_product_quantity_item),
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "Ensure all the fields are correctly entered")
        self.assertEqual(response.status_code, 400)

    def test_post_product_empty_(self):
        """ Test for posting a single product """
        response = self.client().post(BASE_URL,
                                      data=json.dumps(self.empty_product_quantity_item),
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type='application/json')
        data = json.loads(response.data.decode())
        print(data)
        self.assertEqual(data['message'],
                         "Ensure all the fields are correctly entered")
        self.assertEqual(response.status_code, 400)

    def test_post_product_empty_price(self):
        """ Test for posting a single product """
        response = self.client().post(BASE_URL,
                                      data=json.dumps(self.empty_product_category_item),
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type='application/json')
        data = json.loads(response.data.decode())
        print(data)
        self.assertEqual(data['message'],
                         "Ensure all the fields are correctly entered")
        self.assertEqual(response.status_code, 400)

    def test_get_all_products_method(self):
        """ Test for getting all products """
        get_all_products = self.client().get(BASE_URL,
                                             headers=dict(Authorization="Bearer "+self.login()),
                                             content_type='application/json')
        self.assertEqual(get_all_products.status_code, 200)

    def test_get_single_product(self):
        """ Test for getting a single product """
        response = self.client().post(BASE_URL,
                                      data=json.dumps(self.product_item),
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type='application/json')

        data = json.loads(response.get_data())
        single_product = self.client().get(SINGLE_PROD_URL.format(data['product']['product_id']),
                                           headers=dict(Authorization="Bearer "+self.login()),
                                           content_type='application/json')
        self.assertEqual(single_product.status_code, 200)

    def tearDown(self):
        Product.product_list = []
