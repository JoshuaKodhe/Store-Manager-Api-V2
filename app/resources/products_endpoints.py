from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_claims
from flask_expects_json import expects_json

from app.models.products_model import Product
from app.validators.input_validators import InputValidator
from app.utils.schema import product_schema


class ProductEndpoint(Resource):
    @jwt_required
    @expects_json(product_schema)
    def post(self):
        role = get_jwt_claims()['role']
        if role != "admin":
            return {"message": "You do not have authorization to access this feature"}

        data = request.get_json()

        name = InputValidator.valid_string(data['name'].strip())
        description = InputValidator.valid_string(data['description'].strip())
        category = InputValidator.valid_string(data['category'].strip())
        quantity = InputValidator.valid_number(data['quantity'])
        unit_price = InputValidator.valid_number((data['price']))

        payload = ['name', 'description', 'category', 'quantity', 'price']

        for item in data.keys():
            if item not in payload:
                return {"message": f"The field {item} is not a valid field"}, 400

        if Product.retrieve_product_by_name(name):
            return{"message": f"Product {name} exists"}, 400

        if (name) and description and category and(quantity)and(unit_price):
            new_product = Product(name, category, unit_price, quantity,
                                  description).save()
            return {"product": new_product,
                    "message": "Successfully added"}, 201
        return {"message": "Ensure all the fields are correctly entered"}, 400

    @jwt_required
    def get(self, prod_id):
        """Retrieve a single product"""
        product = Product.retrieve_product_by_id(prod_id)
        if product:
            return {"product": product,
                    "message": "Retrieved successfully"}, 200
        return {"message": f"Product of ID {prod_id} does not exist"}, 404

    @jwt_required
    def put(self, prod_id):
        role = get_jwt_claims()['role']
        if role != "admin":
            return {"message": "You do not have authorization to access this feature"}, 401

        single_product = Product.retrieve_product_by_id(prod_id)
        if not single_product:
            return {"message": f"Product of ID {prod_id} does not exist"}, 404
        data = request.get_json()

        name = single_product['name']
        if 'name' in data:
            name = data['name'].strip()
            product_exists = Product.retrieve_product_by_name(name)
            if product_exists:
                if (product_exists['name']).lower() == ((data['name']).lower()):
                    return {"message": "product name already exists"}, 400
            name = data['name']

        description = single_product['description']
        if 'description' in data:
            description = data['description']
        category = single_product['category']
        if 'category' in data:
            category = data['category']
        price = single_product['price']
        if 'price' in data:
            price = data['price']
        quantity = single_product['quantity']
        if 'quantity' in data:
            quantity = data['quantity']

        single_product = Product.update_product(name, category, price,
                                                quantity, description, prod_id)
        return {"product": single_product,
                "message": "product updated"}, 200

    @jwt_required
    def delete(self, prod_id):
        role = get_jwt_claims()['role']
        if role != "admin":
            return {"message": "You do not have authorization to access this feature"}, 401

        product = Product.retrieve_product_by_id(prod_id)
        if not product:
            return {"message": f"Product of ID {prod_id} does not exist"}, 404

        product = Product.delete_product(prod_id)
        return {"message": f"The product {product['name']} delete!"}, 200


class ProductsEndpoint(Resource):
    @jwt_required
    def get(self):
        products = Product.retrieve_products(self)
        if products:
            return {"products": products,
                    "message": "retrieved successfully"}, 200
