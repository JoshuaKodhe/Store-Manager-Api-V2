import unittest
import json
from app import create_app
from app.models.db_setup import DB

base_url = "/api/v2"


class BaseTest(unittest.TestCase):
	'''Set up method to create an attendant, admin, product,
	and a sales table for use in other tests and authentication'''

	def setUp(self):
		self.app = create_app(config_name="testing")
		self.db = DB("testing")
		self.db.create_tables()
		self.client = self.app.test_client()
		self.app_context = self.app.app_context()
		self.app_context.push()

		# Auth variables

		self.proper_reg = json.dumps({"email": "testuser@gmail.com",
									  "username": "testU",
									  "password": "asdfg",
									  "role": "attendant"
									  })
		self.blank_email_reg = json.dumps({"email": " ",
										   "username": "testU",
										   "password": "asdfg",
										   "role": "attendant"
										   })
		self.empty_pass_reg = json.dumps({"email": "test@gmail.com",
										  "username": "testU",
										  "password": " ",
										  "role": "attendant"
										  })
		self.extra_field = json.dumps({"email": "testuser@gmail.com",
									   "username": "testU",
									   "password": "asdfg",
									   "role": "attendant",
									   "age": 34,
									   })

		self.user_login = json.dumps({"email": "testuser@gmail.com",
									  "password": "asdfg",
									  })
		self.empty_email_login = json.dumps({"email": " ",
											 "password": "asdfg",
											 })

		self.empty_pass_login = json.dumps({"email": "testuser@gmail.com",
											"password": " ",
											})

		self.wrong_email_login = json.dumps({"email": "none@gmail.com",
											 "password": "asdfg"
											 })

		self.wrong_pass_login = json.dumps({"email": "testuser@gmail.com",
											"password": "dasfg"
											})

		# products variables

		self.poper_product = json.dumps({"name": "chair",
										 "category": "furniture",
										 "price": 200,
										 "quantity": 15,
										 "description": "great quality"})
		self.poper_product_2 = json.dumps({"name": "Table",
										   "category": "furniture",
										   "price": 200,
										   "quantity": 15,
										   "description": "great quality"})

		self.no_product_name = json.dumps({"name": " ",
										   "category": "furniture",
										   "price": 200,
										   "quantity": 15,
										   "description": "great quality"})

		self.no_pord_category = json.dumps({"name": "chair",
											"category": " ",
											"price": 200,
											"quantity": 15,
											"description": "great quality"})

		self.no_product_price = json.dumps({"name": "chair",
											"category": "furniture",
											"another": "another_one",
											"price": " ",
											"quantity": 15,
											"description": "great quality"})

		self.change_name = json.dumps({"name": "Table",
									   "category": "furniture",
									   "price": 200,
									   "quantity": 15,
									   "description": "great quality"})

	def admin_login(self):
		response = self.client.post(base_url+"/auth/login",
									data=json.dumps({"email":"jkodhe32@gmail.com",
									"password":"joshua123"}),
									content_type="application/json")
		admin_access_token = json.loads(response.get_data())["access_token"]
		return admin_access_token


	def register(self):
		response = self.client.post(base_url+"/auth/register",
									data=self.proper_reg,
									headers=dict(Authorization="Bearer "+self.admin_login()),
									content_type='application/json')

		return response

	def register_attendant_2(self):
		response = self.client.post(base_url+"/auth/register",
									data=json.dumps({
									  "email": "testuser2@gmail.com",
									  "username": "testU2",
									  "password": "qwerty",
									  "role": "attendant"
									}),
									headers=dict(Authorization="Bearer "+self.admin_login()),
									content_type='application/json')
		return response
	
	def login(self):
		self.register()
		response = self.client.post(base_url+"/auth/login",
									data=self.user_login,
									content_type='application/json')
		access_token = json.loads(response.get_data())["access_token"]
		return access_token

	def login_attendant_2(self):
		self.register_attendant_2()
		response = self.client.post(base_url+"/auth/login",
									data=json.dumps({
										"email":"testuser2@gmail.com",
										"password":"qwerty"
									}),
									content_type='application/json')
		access_token = json.loads(response.get_data())["access_token"]
		return access_token


	def post_product(self):
		response = self.client.post(base_url+"/products",
									data=self.poper_product,
									headers=dict(Authorization="Bearer "+self.admin_login()),
									content_type='application/json')
		return response

	def post_another_product(self):
		response = self.client.post(base_url+"/products",
									data=self.poper_product_2,
									headers=dict(Authorization="Bearer "+self.admin_login()),
									content_type='application/json')
		return response

	def make_sale(self):
		response = self.client.post(base_url+"/sales",
									data=json.dumps({"quantity":6,
													 "name":"chair"
									}),
									headers=dict(Authorization="Bearer "+self.login()),
									content_type='application/json')

		return response

	def make_sale_2(self):
		response = self.client.post(base_url+"/sales",
									data=json.dumps({"quantity":2,
													 "name":"chair"
									}),
									headers=dict(Authorization="Bearer "+self.login_attendant_2()),
									content_type='application/json')
		return response

	def tearDown(self):
		'''Method to clear all tables
		before another test is undertaken'''
		self.db.destroy_tables()
		self.app_context.pop()
