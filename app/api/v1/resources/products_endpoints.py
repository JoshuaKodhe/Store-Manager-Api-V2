from flask_restful import Resource
from flask import request, json
from flask_jwt_extended import jwt_required

from app.api.v1.models.products_model import Product
from app.validators.input_validators import InputValidator


class ProductEndpoint(Resource):
    @jwt_required
    def post(self):
        data = request.get_json()

        name = InputValidator.valid_string(data['name'].strip())
        description = InputValidator.valid_string(data['description'].strip())
        category = InputValidator.valid_string(data['category'].strip())
        quantity = InputValidator.valid_number(data['quantity'])
        unit_price = InputValidator.valid_number((data['unit price']))

        payload = ['name', 'description', 'category', 'quantity', 'unit price']

        for item in data.keys():
            if item not in payload:
                return {"message": f"The field {item} is not a valid field"}, 400

        if Product.retrieve_single_products_by_name(self, name):
            return{"message": f"Product {name} exists"}, 400

        if (name) and description and category and(quantity)and(unit_price):
            new_product = Product(name, description, quantity, unit_price, category)
            added_product = new_product.save_product()
            return {"product": added_product}, 201
        return {"message": "Ensure all the fields are correctly entered"}, 400

    @jwt_required
    def get(self, productId):
        single_product = Product.retrieve_single_products(self, productId)
        if single_product:
            return {"product": single_product}, 200
        return {"message": f"Product of ID {productId} does not exist"}, 404

    @jwt_required
    def put(self, productId):
        data = json.loads(request.get_data())
        name = InputValidator.valid_string(data['name'].strip())
        description = InputValidator.valid_string(data['description'].strip())
        category = InputValidator.valid_string(data['category'].strip())
        quantity = InputValidator.valid_number(data['quantity'])
        unit_price = InputValidator.valid_number((data['unit price']))

        payload = ['name', 'description', 'category', 'quantity', 'unit price']

        for item in data.keys():
            if item not in payload:
                return {"message": f"The field {item} is not a valid field"}, 400

        single_product = Product.retrieve_single_products(self, productId)
        if single_product:
            if (name) and description and category and(quantity)and(unit_price):
                single_product = Product.update_product(self, name, description, category, quantity, unit_price)
                return {"product": single_product}, 200
            return {"Ensure that all fields are correct"}, 204
        return {"message": "The product of {productId} does not exist"}, 404


class ProductListEndpoint(Resource):
    @jwt_required
    def get(self):
        all_products = Product.retrieve_products(self)
        return {"Products": all_products,
                "message": "Request succefull"
                }
