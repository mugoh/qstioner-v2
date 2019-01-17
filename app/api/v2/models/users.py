"""
    This file contains the model for users data.
"""
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app as app

from .abstract_model import AbstractModel
from ..database.queries import *


class UserModel(AbstractModel):

    def __init__(self, **kwargs):

        super().__init__()
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.othername = kwargs.get('lastname')
        self.email = kwargs.get('email')
        self.phonenumber = kwargs.get('phonenumber')
        self.username = kwargs.get('username')
        self.isAdmin = kwargs.get('isadmin')
        self.veirified_pass = kwargs.get('password')

        self.password = kwargs.get('password')

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pswd):
        self._password = generate_password_hash(pswd)

    def check_password(self, pass_value):
        # pass_db = self.verify_pass(GET_USER_PASS)
        return check_password_hash(self.veirified_pass, pass_value)

    def save(self):
        return super().save(CREATE_USER,
                            (self.firstname,
                             self.lastname,
                             self.othername,
                             self.email,
                             self.phonenumber,
                             self.username,
                             self.isAdmin,
                             self.password))

    # def verify_pass(self, statement):
    #    return super.get_by_name(statement)

    #
    # Search behaviours

    @classmethod
    def get_by_name(cls, username, key_values=False):
        found_user = super().get_by_name(GET_USER_BY_NAME, (username,))
        print(found_user)

        if key_values and found_user:
            return cls.zipToDict(keys, found_user, single=True)

        elif found_user:
            return UserModel(
                **cls.zipToDict(
                    keys, found_user, single=True))
        return None

    @classmethod
    def get_by_email(cls, given_email):
        user = super().get_by_name(GET_BY_EMAIL, (given_email,))
        if user:
            return UserModel(**cls.zipToDict(keys, user, single=True))
        return None

    @classmethod
    def get_by_id(cls, usr_id):
        usr = super().get_by_id(GET_USER_BY_ID, (usr_id,))

        return UserModel(**cls.zipToDict(
            keys, usr, single=True)) if usr else None

    def encode_auth_token(self, user_name):
        """
            Creates and returns an encoded authorization token.
            It uses the UserModel username attribute as the token identifier.
        """

        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(
                days=app.config.get('AUTH_TOKEN_EXP_DAYS'),
                seconds=app.config.get('AUTH_TOKEN_EXP_SECS')),
            "iat": datetime.datetime.utcnow(),
            "sub": user_name
        }

        return jwt.encode(
            payload,
            app.config['SECRET_KEY'],
            algorithm='HS256')

    @classmethod
    def decode_auth_token(cls, encoded_token):
        """
            Decodes the authorzation token to get the payload
            the retrieves the username from 'sub' attribute
        """
        try:
            payload = jwt.decode(encoded_token,
                                 app.config.get('SECRET_KEY'),
                                 algorithms='HS256')
            return payload['sub']

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as er:
            return {
                "Status": 400,
                "Message": "Token Invalid. Please log in again" + er
            }, 400

    def dictify(self):

        return {
            "Firstname": self.firstname,
            "Lastname": self.lastname,
            "Othername": self.othername,
            "Email": self.email,
            "Phonenumber": self.phonenumber,
            "Username": self.username,
            "isAdmin": self.isAdmin,
            "registered": self.created_at,
        }

        # return self.__dict__

    def __repr__(self):
        return '{Email} {Username}'.format(**self.dictify())


keys = ["id", "firstname", "lastname", "othername", "email",
        "phonenumber", "username", "isadmin", "password"]
