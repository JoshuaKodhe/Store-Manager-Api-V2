""" User authentication """
import datetime
from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required

from app.models.user import User
from app.validators.input_validators import InputValidator


class UserRegistrationEndpoint(Resource):
    """Endpoint for user to register"""
    def post(self):
        data = request.get_json()

        email = InputValidator.valid_email(data['email'].strip())
        username = data['username'].strip()
        password = data['password'].strip()

        payload = ['email', 'username', 'password']

        for item in data.keys():
            if item not in payload:
                return {"message": f"The field {item} is not a valid field"}, 400


        if not email:
            return{"message": "Please enter a valid email"}, 400
        elif not username:
            return {"message": "Please enter a username"}, 400
        elif not password:
            return {"message": "please enter password"}, 400
        else:
            if not User.check_if_user_exists(email):
                new_user = User(email=data['email'],
                                password=User.generate_hash(data['password'])
                                )
                new_user.save_user()
                return {"message": f'User {data["email"]} was created'}, 201
            return {"message": f"User {email} already exists"}, 400
        return {"message": 'Please enter an email address and password',
                }, 400


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = InputValidator.valid_email(data['email'].strip())
        password = data['password'].strip()

        payload = ['email', 'password']

        for item in data.keys():
            if item not in payload:
                return {"message": f"The field {item} is not a valid field"}, 400

        if email and password:
            if User.fetch_single_user(self, email):
                current_user = User.fetch_single_user(self, email)
                if User.verify_hash(password,
                                    current_user[2]):
                    access_token = create_access_token(identity=email,
                                                       expires_delta=datetime.timedelta(hours=1))
                    return{'message': f'Logged in as {current_user[1]}',
                           'access_token': access_token,
                           }, 200
                return {'message': 'Invalid password'}, 400
            return {'message': 'User does not exist'}, 404
        return {"message": "Enter email and password to login"}, 400


class UserLogout(Resource):
    @jwt_required
    def delete(self):
        blacklist = set()
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"message": "Successfully logged out"}, 200
