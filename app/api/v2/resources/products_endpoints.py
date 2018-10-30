from flask_restful import Resource
from flask import request, json
from flask_jwt_extended import jwt_required

from app.api.v2.models.products_model import Product
from app.validators.input_validators import InputValidator


class ProductEndpoint(Resource):
    def post(self):
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

        # if Product.retrieve_single_products_by_name(self, name):
        #     return{"message": f"Product {name} exists"}, 400

        if (name) and description and category and(quantity)and(unit_price):
            new_product = Product(name, description, quantity, unit_price, category).save()
            return {"product": new_product,
                    "message": "Successfully added"}, 201
        return {"message": "Ensure all the fields are correctly entered"}, 400
