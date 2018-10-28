""" Create our application """
from flask import Flask
from flask_jwt_extended import JWTManager

from instance.config import APP_CONFIG
from app.api.v1 import VERSION_1 as v1
from app.api.v2 import VERSION_2 as v2

JWT = JWTManager()


def create_app(config_name):
    """ Registering app confingurations """
    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[config_name])

    app.register_blueprint(v1)

    app.register_blueprint(v2)

    JWT.init_app(app)
    return app
