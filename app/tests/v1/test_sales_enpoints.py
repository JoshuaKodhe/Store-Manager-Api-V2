import unittest
from flask import json
from app import create_app
from app.api.v1.models.sales_models import SaleRecordModel

BASE_URL = '/api/v1/sales'
SINGLE_SALE_URL = '/api/v1/sales/{}'
LOGIN_URL = '/api/v1/auth/login'

PROD_BASE_URL = '/api/v1/products'


class TestSalesEndpoints(unittest.TestCase):
    """class to test the sales endpoints"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.product_item = {"name": "Table",
                             "description": "The product description here",
                             "quantity": 12,
                             "category": "Furniture",
                             "unit price": 2000}

        self.sale_record = {"sale_attendant": "Kay Jay",
                            "product_name": "Table",
                            "quantity": 2
                            }

        self.login_user = {"email": "testuser@gmail.com",
                           "password": "asdfg",
                           }

    def login(self):
        response = self.client().post(LOGIN_URL,
                                      data=json.dumps(self.login_user),
                                      content_type='application/json')

        access_token = json.loads(response.data.decode())["access_token"]
        return access_token

    def test_post_single_sale_record(self):
        """ Testing post a sale record """
        post_product = self.client().post(PROD_BASE_URL,
                                          data=json.dumps(self.product_item),
                                          headers=dict(Authorization="Bearer "+self.login()),
                                          content_type='application/json')
        response = self.client().post(BASE_URL,
                                      data=json.dumps(self.sale_record),
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type="application/json")

        self.assertEqual(response.status_code, 201)

    def test_get_single_sale_record(self):
        """ Test get a sale record """
        post_product = self.client().post(PROD_BASE_URL,
                                          data=json.dumps(self.product_item),
                                          headers=dict(Authorization="Bearer "+self.login()),
                                          content_type='application/json')
        response = self.client().post(BASE_URL,
                                      data=json.dumps(self.sale_record),
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type="application/json")

        data = json.loads(response.get_data())
        print(data)
        single_sale_record = self.client().get(SINGLE_SALE_URL.format(data['sale record']['sale_id']),
                                               headers=dict(Authorization="Bearer "+self.login()),
                                               content_type="application/json")
        self.assertEqual(single_sale_record.status_code, 200)

    def test_get_all_sale_records_method(self):
        """ Test for getting all products """
        get_all_sale_records = self.client().get(BASE_URL,
                                                 headers=dict(Authorization="Bearer "+self.login()),
                                                 content_type="application/json")
        self.assertEqual(get_all_sale_records.status_code, 200)

    def tearDown(self):
        SaleRecordModel.product_list = []
