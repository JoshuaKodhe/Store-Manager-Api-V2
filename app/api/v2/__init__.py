""" Register Blueprints and our routes """
from flask import Blueprint
from flask_restful import Api


from app.api.v2.resources.products_endpoints import ProductEndpoint


VERSION_2 = Blueprint('API2', __name__, url_prefix="/api/v2")
API = Api(VERSION_2)

API.add_resource(ProductEndpoint, '/products', '/products/<int:productId>')
