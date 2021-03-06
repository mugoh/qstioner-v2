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
from ..database.queries import GET_ALL_USERS


class UsersRegistration(Resource):
    """
        This resource allows a user to create a new account.
    """

    @swag_from('docs/auth_register.yml')
    def post(self):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)
        parser.add_argument('firstname', type=verify_name, required=True)
        parser.add_argument('lastname', type=verify_name, required=True)
        parser.add_argument('othername', type=verify_name)
        parser.add_argument('email', type=inputs.regex(
            r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$"), required=True,
            help="Oopsy! Email format not invented yet")
        parser.add_argument('phonenumber', type=int, required=True)
        parser.add_argument('username', type=verify_name, required=True)
        parser.add_argument('isadmin', type=bool, default=False)
        parser.add_argument('password', required=True, type=verify_pass)

        args = parser.parse_args(strict=True)

        if UserModel.get_by_email(args.get('email')):
            return {
                "status": 409,
                "message": "Account exists. Maybe log in?"
            }, 409

        if UserModel.get_by_name(args.get('username')):
            return {
                "status": 409,
                "message": "Oopsy! username exists.Try " +
                args.get('username') + str(random.randint(0, 40))
            }, 409

        user = UserModel(**args)
        _usr = user.save()

        return {
            "status": 201,
            "message": "Registration Success",
            "data": UserModel.zipToDict(keys, _usr, single=True)
        }, 201

    @swag_from('docs/auth_get_users.yml')
    def get(self):
        """
            Retrieves existing registered users
        """

        data = UserModel.get_all(GET_ALL_USERS)
        if data:
            data = UserModel.zipToDict(keys, data)
        return {
            "status": 200,
            "data": data
        }, 200


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
                "status": 404,
                "message": "Email or password Incorrect"
            }, 404

        elif not user.check_password(args.get('password')):
            return {
                "status": 403,
                "message": "Incorrect email or password." +
                "Try again"
            }, 403

        return {
            "status": 200,
            "data": [{"message": f"Logged in as {user.username}",
                      "token": user.encode_auth_token(
                          user.username).decode('utf-8'),
                      "user": repr(user),
                      "isadmin": user.isAdmin}]
        }, 200


class UserLogout(Resource):

    @auth_required
    @swag_from('docs/auth_logout.yml')
    def delete(this_user, self):
        payload = get_raw_auth()
        Token(payload)  # Blaclist current user token
        return {
            "status": "Success",
            "message": f"Logout {get_auth_identity()}"
        }, 200


keys = ["id", "firstname", "lastname", "othername", "email",
        "phonenumber", "username", "isadmin"]

USER_SCHEMA = {
    'type': 'object',
    'maxProperties': 3,
    'properties': {
        'email': {'type': 'string'},
        'username': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['email', 'password']}
