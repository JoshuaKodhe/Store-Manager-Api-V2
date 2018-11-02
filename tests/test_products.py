from flask import json
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

    def test_get_products_succesfully(self):
        '''Tests for no price'''
        self.post_product()

        response = self.client.get(base_url+"/products",
                                   headers=dict(Authorization="Bearer "+self.login()),
                                   content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "retrieved successfully")
        self.assertEqual(response.status_code, 200)

    def test_get_single_product_succesfully(self):
        '''Tests for no price'''
        self.post_product()

        response = self.client.get(base_url+"/products/1",
                                   headers=dict(Authorization="Bearer "+self.login()),
                                   content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "Retrieved successfully")
        self.assertEqual(response.status_code, 200)

    def test_get_single_product_fail(self):
        '''Tests for no price'''
        self.post_product()

        response = self.client.get(base_url+"/products/5",
                                   headers=dict(Authorization="Bearer "+self.login()),
                                   content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "Product of ID 5 does not exist")
        self.assertEqual(response.status_code, 404)

    def test_delete_product_fail(self):
        '''Tests for no price'''
        self.post_product()

        response = self.client.delete(base_url+"/products/5",
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "Product of ID 5 does not exist")
        self.assertEqual(response.status_code, 404)

    def test_delete_product(self):
        '''Tests for no price'''
        self.post_product()
        response = self.client.delete(base_url+"/products/1",
                                      headers=dict(Authorization="Bearer "+self.login()),
                                      content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],
                         "The product chair delete!")
        self.assertEqual(response.status_code, 200)

    def test_update_product_fail(self):
        '''Tests for no price'''
        self.post_product()
        response = self.client.put(base_url+"/products/4",
                                   data=self.change_name,
                                   headers=dict(Authorization="Bearer "+self.login()),
                                   content_type='application/json')
        data = json.loads(response.data.decode())
        print(data)
        self.assertEqual(data['message'],
                         "Product of ID 4 does not exist")
        self.assertEqual(response.status_code, 404)

    def test_update_product_name_exists(self):
        '''Tests for no price'''
        self.post_product()
        self.post_another_product()
        response = self.client.put(base_url+"/products/1",
                                   data=self.change_name,
                                   headers=dict(Authorization="Bearer "+self.login()),
                                   content_type='application/json')
        data = json.loads(response.data.decode())
        print(data)
        self.assertEqual(data['message'],
                         "product name already exists")
        self.assertEqual(response.status_code, 400)

    def test_update_product(self):
        '''Tests for no price'''
        self.post_product()
        response = self.client.put(base_url+"/products/1",
                                   data=self.change_name,
                                   headers=dict(Authorization="Bearer "+self.login()),
                                   content_type='application/json')
        data = json.loads(response.data.decode())
        print(data)
        self.assertEqual(data['message'],
                         "product updated")
        self.assertEqual(response.status_code, 200)
