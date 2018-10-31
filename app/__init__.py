""" Create our application """
from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager

from instance.config import APP_CONFIG
from app.models.db_setup import DB

from app.resources.products_endpoints import ProductEndpoint

from app.resources.auth_endpoints import (UserRegistrationEndpoint,
                                          UserLogin, UserLogout)

JWT = JWTManager()


def create_app(config_name):
    """ Registering app confingurations """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name])

    db = DB(config_name)
    db.create_tables()

    version_2 = Blueprint('api2', __name__, url_prefix="/api/v2")
    api = Api(version_2)

    api.add_resource(ProductEndpoint, '/products', '/products/<int:productId>')
    api.add_resource(UserRegistrationEndpoint, '/auth/register')
    api.add_resource(UserLogin, '/auth/login')
    api.add_resource(UserLogout, '/auth/logout')

    app.register_blueprint(version_2)

    JWT.init_app(app)
    return app
