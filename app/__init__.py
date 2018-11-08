""" Create our application """
from flask import Flask
from flask_jwt_extended import JWTManager

from instance.config import APP_CONFIG
from app.v2.models.db_setup import DB

JWT = JWTManager()


def create_app(config_name):
    """ Registering app confingurations """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(APP_CONFIG[config_name])

    db = DB(config_name)
    db.create_tables()

    from app.v2 import VERSION_2 as v2
    app.register_blueprint(v2)

    JWT.init_app(app)
    return app
