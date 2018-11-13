from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from flask_expects_json import expects_json

from app.models.sales import Sales
from app.models.products_model import Product
from app.validators.input_validators import InputValidator
from app.utils.schema import sale_schema


class SalesRecordEnpoint(Resource):
	@jwt_required
	@expects_json(sale_schema)
	def post(self):
		""" Post a sale_record """
		data = request.get_json()

		sale_attendant = get_jwt_identity()['email']
		name = InputValidator.valid_string(data['name'].strip())
		quantity_to_sell = InputValidator.valid_number(data['quantity'])
		payload = ['name', 'quantity']

		for item in data.keys():
			if item not in payload:
				return {"message": f"The field {item} is not a valid field"}, 400

		if Product.retrieve_product_by_name(name):
			product_on_sale = Product.retrieve_product_by_name(name)
			if quantity_to_sell <= product_on_sale["quantity"]:
				total = product_on_sale["price"] * quantity_to_sell
				new_sale_record = Sales(quantity_to_sell,
										name, sale_attendant, total)

				added_sale_record = new_sale_record.save_record()
				Product.update_product(name,
									   product_on_sale["category"],
									   product_on_sale["price"],
									   product_on_sale["quantity"]-quantity_to_sell,
									   product_on_sale['description'],
									   product_on_sale['prod_id'],
									   )
				new_quantity = product_on_sale["quantity"]-quantity_to_sell
				return {"sale record": added_sale_record,
						"message": f"The quantity of {product_on_sale['name']} has been updated new quantity is {new_quantity}"}, 200
			return {"message": f"The quantity you entered exceeds stoked quantity"}, 400
		return {"message": f"product {name} does not exist"}, 404

	@jwt_required
	def get(self, sale_id):
		"""Retrieve a single sales"""
		user = get_jwt_identity()['email']
		role = get_jwt_claims()['role']
		sales = Sales.retrieve_sales_by_id(sale_id)
		print(sales)

		if sales:
			if (role == "admin") or (user == sales['sale_attendant']):
				return {"sale_records": sales,
						"message": "Retrieved successfully"}, 200
			return {"message": "You do not have authorization to access the sale record"}, 401
		return {"message": f"Sale of ID {sale_id} does not exist"}, 404


class SalesRecordsEnpoint(Resource):
	@jwt_required
	def get(self):
		role = get_jwt_claims()['role']
		if role == "admin":
			sales_records = Sales.retrieve_sales()
			if sales_records:
				return {"sales_records": sales_records,
						"message": "retrieved successfully"}, 200
		else:
			user = get_jwt_identity()['email']
			sales_records = Sales.retrieve_sales_by_attendant(user)
			if sales_records:
				return {"sales_records": sales_records,
						"message": "retrieved successfully"}, 200
