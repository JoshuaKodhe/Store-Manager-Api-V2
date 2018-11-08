""" User authentication """

from flask_restful import Resource
from flask import request


from app.v2.models.user import User
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
