"""
    This file contains the model for users data.
"""
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from flask import current_app as app

from .abstract_model import AbstractModel


class UserModel(AbstractModel):

    def __init__(self, *kwargs):

        super().__init__()
        self.firstname = kwargs[0]
        self.lastname = kwargs[1]
        self.othername = kwargs[2]
        self.email = kwargs[3]
        self.phonenumber = kwargs[4]
        self.username = kwargs[5]
        self.isAdmin = kwargs[6]

        self.password = kwargs[7]

    @property
    def password(self):
        return '****'

    @password.setter
    def password(self, pswd):
        self._password = generate_password_hash(pswd)

    def check_password(self, pass_value):

        return check_password_hash(self._password, pass_value)

    def save(self):
        return super().save(CREATE_USER,
                            (self.firstname,
                             self.lastname,
                             self.othername,
                             self.email,
                             self.password,
                             self.username,
                             self.isAdmin,
                             self.phonenumber))

    #
    # Search behaviours

    @classmethod
    def get_by_name(cls, username):
        found_user = super().get_by_name(GET_USER_BY_NAME, username)

        return UserModel(*found_user) if found_user else None

    @classmethod
    def get_by_email(cls, given_email):
        user = super().get_by_name(GET_BY_EMAIL, given_email)

        return UserModel(*user) if user else None

    @classmethod
    def get_by_id(cls, usr_id):
        usr = super().get_by_id(GET_USER_BY_ID, usr_id)

        return UserModel(*usr) if usr else None

    @classmethod
    def get_all_users(cls):
        return [user.dictify() for user in users]

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
            "password": self.password,
            "registered": self.created_at,
            "id": self.id
        }

        # return self.__dict__

    def __repr__(self):
        return '{Email} {Username}'.format(**self.dictify())
