"""
    This file conntains views for all the user endpoints
"""

from flask_restful import Resource, reqparse, inputs
from flasgger import swag_from
import random

from ..models.users import UserModel
from ..models.tokens import Token
from ..utils.helpers import verify_pass, verify_name
from ..utils.auth import auth_required, get_raw_auth, get_auth_identity


class UsersRegistration(Resource):
    """
        This resource allows a user to create a new account.
    """

    @swag_from('docs/auth_register.yml')
    def post(self):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)
        parser.add_argument('firstname', type=verify_name)
        parser.add_argument('lastname', type=verify_name)
        parser.add_argument('othername', type=verify_name)
        parser.add_argument('email', type=inputs.regex(
            r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$"), required=True,
            help="Oopsy! Email format not invented yet")
        parser.add_argument('phonenumber', type=int)
        parser.add_argument('username', type=verify_name)
        parser.add_argument('isAdmin', type=bool, default=False)
        parser.add_argument('password', required=True, type=verify_pass)

        args = parser.parse_args(strict=True)

        if UserModel.get_by_email(args.get('email')):
            return {
                "Status": 409,
                "Message": "Account exists. Maybe log in?"
            }, 409

        if UserModel.get_by_name(args.get('username')):
            return {
                "Status": 409,
                "Message": "Oopsy! username exists.Try " +
                args.get('username') + str(random.randint(0, 40))
            }, 409

        user = UserModel(**args)
        user.save()

        return {
            "Status": 201,
            "Data": user.dictify()
        }

    @swag_from('docs/auth_get_users.yml')
    def get(self):
        return {
            "Status": 200,
            "Data": UserModel.get_all_users()
        }


class UserLogin(Resource):

    @swag_from('docs/login.yml')
    def post(self):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)

        parser.add_argument('email', type=inputs.regex(
            r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$"), required=True,
            help="Please provide a valid email. Cool?")
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('username', type=verify_name)

        args = parser.parse_args(strict=True)

        user = UserModel.get_by_email(args.get('email'))

        if not user:
            return {
                "Status": 404,
                "Message": "Account unknown. Maybe register?"
            }, 404

        elif not user.check_password(args.get('password')):
            return {
                "Status": 403,
                "Message": "Incorrect password.\
                        Please give me the right thing, okay?"
            }, 403

        return {
            "Status": 200,
            "Data": [{"Message": f"Logged in as {user.username}",
                      "token": str(user.encode_auth_token(user.username)),
                      "user": repr(user)}]
        }, 200


class UserLogout(Resource):

    @auth_required
    @swag_from('docs/auth_logout.yml')
    def delete(this_user, self):
        payload = get_raw_auth()
        Token(payload)  # Blaclist current user token
        return {
            "Status": "Success",
            "Message": f"Logout {get_auth_identity()}"
        }, 200


USER_SCHEMA = {
    'type': 'object',
    'maxProperties': 3,
    'properties': {
        'email': {'type': 'string'},
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password']}
