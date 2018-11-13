from flask import json
from .base_test import BaseTest, base_url


class TestAuthRegistratio(BaseTest):
	def test_registration_by_admin(self):
		"""Test registration when all the fields are present"""
		response = self.register()
		data = json.loads(response.data.decode())

		self.assertEqual(data['message'],
						 "User testuser@gmail.com was created")
		self.assertEqual(response.status_code, 201)

	def test_registration_by_non_admin(self):
		"""Test registration when all the fields are present"""
		response = self.client.post(base_url+"/auth/register",
									data=self.proper_reg,
									headers=dict(Authorization="Bearer "+self.login()),
									content_type='application/json')
		data = json.loads(response.data.decode())

		self.assertEqual(data['message'],
						 "You do not have authorization to access this feature")
		self.assertEqual(response.status_code, 401)

	def test_empty_email_register(self):
		"""Test registration when the email field is missing"""
		response = self.client.post(base_url+"/auth/register",
									data=self.blank_email_reg,
									headers=dict(Authorization="Bearer "+self.admin_login()),
									content_type='application/json')
		data = json.loads(response.data.decode())

		self.assertEqual(data['message'],
						 "Please enter a valid email")
		self.assertEqual(response.status_code, 400)

	def test_empty_password_register(self):
		"""Test registration when the password field is missing"""
		response = self.client.post(base_url+"/auth/register",
									data=self.empty_pass_reg,
									headers=dict(Authorization="Bearer "+self.admin_login()),
									content_type='application/json')
		data = json.loads(response.data.decode())
		self.assertEqual(data['message'],
						 "please enter password")
		self.assertEqual(response.status_code, 400)

	def test_existing_email_register(self):
		"""Test registration when the email exists"""
		self.register()
		response = self.register()
		data = json.loads(response.data.decode())
		self.assertEqual(data['message'],
						 "User testuser@gmail.com already exists")
		self.assertEqual(response.status_code, 400)

	def test_extra_field_in_payload(self):
		"""Test registration when all the fields are present"""
		response = self.client.post(base_url+"/auth/register",
									data=self.extra_field,
									headers=dict(Authorization="Bearer "+self.admin_login()),
									content_type='application/json')
		data = json.loads(response.data.decode())

		self.assertEqual(data['message'],
						 "The field age is not a valid field")
		self.assertEqual(response.status_code, 400)
