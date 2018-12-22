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
            return {"message": "You do not have authorization to access this feature"}, 401

        data = request.get_json()

        name = InputValidator.valid_string(data['name'].strip())
        description = InputValidator.valid_string(data['description'].strip())
        category = InputValidator.valid_string(data['category'].strip())
        quantity = InputValidator.valid_number(data['quantity'])
        unit_price = InputValidator.valid_number((data['price']))
        image_url = InputValidator.valid_image(data['image_url'].strip())

        payload = ['name', 'description', 'category',
                   'quantity', 'price', 'image_url']

        for item in data.keys():
            if item not in payload:
                return {"message": f"The field {item} is not a valid field"}, 400

        if Product.retrieve_product_by_name(name):
            return{"message": f"Product {name} exists"}, 400
        else:
            if not name:
                return {"message": "Field name should contain letters"}, 400
            elif not description:
                return {"message": "Field description should contain letters"}, 400
            elif not category:
                return {"message": "Field category should contain letters"}, 400
            elif not quantity:
                return {"message": "Field should contain numbers"}, 400
            elif not unit_price:
                return {"message": "Field unit_price should contain number"}, 400
            elif not image_url:
                return {"message": "Field image_url should contain url"}, 400
            else:
                new_product = Product(name, category, unit_price, quantity,
                                      description, image_url).save()
                return {"product": new_product,
                        "message": "Successfully added"}, 201

    @jwt_required
    def get(self, prod_id):
        """Retrieve a single product"""
        role = get_jwt_claims()['role']
        product = Product.retrieve_product_by_id(prod_id)
        if product:
            return {"product": product,
                    "role": role,
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
        description = single_product['description']
        category = single_product['category']
        price = single_product['price']
        quantity = single_product['quantity']
        image_url = single_product['image_url']

        if 'name' in data:
            name = InputValidator.valid_string(data['name'].strip())
            if not name:
                return {"message": "Field name should contain letters"}, 400

        if 'description' in data:
            description = InputValidator.valid_string(
                data['description'].strip())
            if not description:
                return {"message": "Field description should contain letters"}, 400

        if 'category' in data:
            category = InputValidator.valid_string(data['category'].strip())
            if not category:
                return {"message": "Field category should contain letters"}, 400

        if 'price' in data:
            price = InputValidator.valid_number((data['price']))
            if not price:
                return {"message": "Field price should contain number"}, 400

        if 'quantity' in data:
            quantity = InputValidator.valid_number((data['price']))
            if not quantity:
                return {"message": "Field quantity should contain numbers"}, 400

        if 'image_url' in data:
            image_url = InputValidator.valid_image(
                data['image_url'].strip())
            if not image_url:
                return {"message": "Field image_url should contain url"}, 400

        single_product = Product.update_product(name, category, price,
                                                quantity, description, image_url, prod_id)
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
        return {"message": f"The product of ID {prod_id} was delete!"}, 200


class ProductsEndpoint(Resource):
    @jwt_required
    def get(self):
        role = get_jwt_claims()['role']
        products = Product.retrieve_products(self)
        if products:
            return {"products": products,
                    "role": role,
                    "message": "retrieved successfully"}, 200
