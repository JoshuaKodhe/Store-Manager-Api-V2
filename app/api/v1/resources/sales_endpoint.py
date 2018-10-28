from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required

from app.api.v1.models.sales_models import SaleRecordModel
from app.validators.input_validators import InputValidator
from app.api.v1.models.products_model import Product


class SalesRecordEndpoint(Resource):
    @jwt_required
    def post(self):
        """ Post a sale_record """
        data = request.get_json()

        attendant = data['sale_attendant']
        name = InputValidator.valid_string(data['product_name'].strip())
        quantity_to_sell = InputValidator.valid_number(data['quantity'])
        payload = ['sale_attendant', 'product_name', 'quantity']

        for item in data.keys():
            if item not in payload:
                return {"message": f"The field {item} is not a valid field"}, 400

        if Product.retrieve_single_products_by_name(self, name):
            product_on_sale = Product.retrieve_single_products_by_name(self,
                                                                       name)
            print(product_on_sale)
            if quantity_to_sell < product_on_sale["product_quantity"]:
                new_sale_record = SaleRecordModel(attendant,
                                                  name,
                                                  product_on_sale["unit_price"],
                                                  quantity_to_sell,
                                                  product_on_sale["category"])

                added_sale_record = new_sale_record.save_record()

                Product.update_product(self,
                                       name,
                                       product_on_sale['product_description'],
                                       product_on_sale["category"],
                                       product_on_sale["product_quantity"]-quantity_to_sell,
                                       product_on_sale["unit_price"])
                return {"sale record": added_sale_record,
                        "message": f"The quantity of {product_on_sale['product_name']} has been updated"}, 201
            return {"message": f"The quantity you entered exceeds stoked quantity"}, 400
        return {"message": f"product {name} does not exist"}, 404

    @jwt_required
    def get(self, saleId):
        """ Get a single sale_record"""
        sale_record = SaleRecordModel.retrieve_single_records(self, saleId)
        if sale_record:
            return {"sale record": sale_record}, 200
        return {"message": f"Sale record of ID {saleId} doesn't exist"}, 404


class SalesRecordsListEndpoint(Resource):
    @jwt_required
    def get(self):
        sale_records = SaleRecordModel.retrieve_records(self)
        if sale_records:
            return {"sale_records": sale_records,
                    "message": "Request succeful"}, 200
