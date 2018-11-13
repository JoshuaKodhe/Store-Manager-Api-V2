from flask import json
from .base_test import BaseTest, base_url


class TestSale(BaseTest):
	def test_get_sales_by_attendant(self):
		'''Tests for a successful get all sales'''
		response = self.client.get(base_url+"/sales",
								   headers=dict(Authorization="Bearer "+self.login()),
								   content_type='application/json')

		data = json.loads(response.data.decode())
		self.assertEqual(data["message"], "retrieved successfully")
		self.assertEqual(response.status_code, 200)

	def test_get_sales_by_admin(self):
		'''Tests for a successful get all sales'''
		response = self.client.get(base_url+"/sales",
								   headers=dict(Authorization="Bearer "+self.admin_login()),
								   content_type='application/json')

		data = json.loads(response.data.decode())
		self.assertEqual(data["message"], "retrieved successfully")
		self.assertEqual(response.status_code, 200)

	def test_get_sale_by_id_that_does_not_exist(self):
		'''Tests for get a sale by id that does not exist'''
		response = self.client.get(base_url+"/sales/15",
								   headers=dict(Authorization="Bearer "+self.admin_login()),
								   content_type='application/json')
		data = json.loads(response.data.decode())
		self.assertEqual(data["message"], "Sale of ID 15 does not exist")
		self.assertEqual(response.status_code, 404)

	def test_get_sale_by_id_that_exists(self):
		'''Test get sale successful'''
		self.post_product()
		self.make_sale()

		response = self.client.get(base_url+"/sales/1",
								   headers=dict(Authorization="Bearer "+self.admin_login()),
								   content_type='application/json')
		data = json.loads(response.data.decode())
		self.assertEqual(data["message"], "Retrieved successfully")
		self.assertEqual(response.status_code, 200)

	def test_get_sale_by_attendant_that_didnt_make_sale(self):
		self.post_product()
		self.make_sale()
		self.make_sale_2()

		response = self.client.get(base_url+"/sales/2",
								   headers=dict(Authorization="Bearer "+self.login()),
								   content_type='application/json')
		data = json.loads(response.data.decode())
		self.assertEqual(data["message"], "You do not have authorization to access the sale record")
		self.assertEqual(response.status_code, 401)

	def test_make_sale(self):
		self.post_product()
		response = self.make_sale()

		data = json.loads(response.data.decode())
		self.assertEqual(data['message'], "The quantity of chair has been updated new quantity is 9")
		self.assertEqual(response.status_code, 200)