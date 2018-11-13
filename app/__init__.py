""" Create our application """
from flask import Flask, Blueprint, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from instance.config import APP_CONFIG
from app.models.db_setup import DB
from app.resources.products_endpoints import (ProductEndpoint,
											  ProductsEndpoint)
from app.resources.sales_endpoints import (SalesRecordsEnpoint,
										   SalesRecordEnpoint)
from app.resources.auth_endpoints import (UserRegistrationEndpoint,
										  UserLogin, UserLogout)
from app.resources.auth_endpoints import blacklist
from flask_cors import CORS

jwt = JWTManager()


def create_app(config_name):
	""" Registering app confingurations """
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(APP_CONFIG[config_name])

	# db initialization
	db = DB(config_name)
	db.create_tables()
	db.create_admin()

	# cors setup
	CORS(app)

	# jwt claims for role
	jwt.init_app(app)

	@jwt.user_claims_loader
	def add_claims_to_access_token(user_identifier):
		return {'role': user_identifier["role"]}

	@jwt.user_identity_loader
	def user_identity_lookup(user_identifier):
		return {'email': user_identifier["email"]}

	# jwt token revoking
	@jwt.token_in_blacklist_loader
	def check_if_token_in_blacklist(decrypted_token):
		jti = decrypted_token['jti']
		return jti in blacklist

	# registering routes
	version_2 = Blueprint('api2', __name__, url_prefix="/api/v2")
	api = Api(version_2)

	api.add_resource(ProductsEndpoint, '/products')
	api.add_resource(ProductEndpoint, '/products', '/products/<int:prod_id>')
	api.add_resource(SalesRecordsEnpoint, '/sales')
	api.add_resource(SalesRecordEnpoint, '/sales', '/sales/<int:sale_id>')
	api.add_resource(UserRegistrationEndpoint, '/auth/register')
	api.add_resource(UserLogin, '/auth/login')
	api.add_resource(UserLogout, '/auth/logout')

	app.register_blueprint(version_2)

	#error handling
	@app.errorhandler(Exception)
	def unhandled_exception(e):
		return jsonify({"message": "we couldnt find that resource.Please contact the admin"}), 404

	return app
