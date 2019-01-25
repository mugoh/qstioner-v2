"""
    This module contains validators that help with
    Authorization cases.
"""

from functools import wraps
from flask import request

from ...v2.models.users import UserModel
from ..models.tokens import Token

current_user = None
raw_auth = None


def admin_required(f):
    """
        Protects endpoints accessible to admin user only.
        Ensures only an admin user can access this endpoint.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):

        # We never get here in real sense, consumed by missing Auth header
        # Uncomment when testing manually
        #
        # Verify Logged in
        """if not current_user:
            return {
                "status": 403,
                "error": "Please log in, okay?"
            }, 403

        user = UserModel.get_by_name(current_user)
        if not user:
            return {
                "status": 400,
                "error": "Identity unknown"
            }
    """
        current_user = get_auth_identity()

        if not UserModel.get_by_name(current_user).isAdmin:
            return {
                "status": 403,
                "message": "Oops! Only an admin can do that"
            }, 403
        return f(*args, **kwargs)
    return wrapper


def current_user_only(f):
    """
        Ensures the user changing the resource in a protected endpoint
        is the one who created that resource.e.g Deleting a question
    """
    @wraps(f)
    def wrapper(*args, **kwars):
        url_user_field = request.base_url.split('/')
        user = url_user_field[-2]
        this_user = get_auth_identity()

        # Comment out if manually testing
        # Handled by missing auth header error

        """if not this_user:
            return {
                "status": 403,
                "message": "You need to be logged in to do that"
            }, 403
        """
        try:
            uid = int(user)
            user = UserModel.get_by_id(uid)
            if user:
                user = user.username
            else:
                return {
                    "status": 404,
                    "error": "User id does not exist. Provide a valid id"
                }, 404

        except ValueError:
            user = user
            if not UserModel.get_by_name(user):
                return {
                    "status": 404,
                    "error": "Username not registered. \
                    Provide a valid username"
                }, 404

        if this_user != user:
            return {
                "status": 403,
                "error": "Denied. Not accessible to current user"
            }, 403
        return f(*args, **kwars)
    return wrapper


def auth_required(f):
    """
        Protects endpoints that require user authrorization for access
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return {
                "status": 400,
                "message": "Please provide a valid Authorization Header"
            }, 400

        auth_header = request.headers['Authorization']

        try:
            payload = auth_header.split(' ')[1]
        except IndexError:

            return {
                "status": 400,
                "message": "Please provide a valid Authorization Header"
            }, 400

        if not payload:
            return {
                "status": 400,
                "message": "Token is empty. Please provide a valid token"
            }, 400

        if Token.check_if_blacklisted(payload):
            return {
                "status": 400,
                "message": "Token unsuable. Try signing in again"
            }, 400

        try:
            user_identity = UserModel.decode_auth_token(payload)

            current_user = UserModel.get_by_name(user_identity).username
            save_raw_payload(payload, current_user)

        except Exception:
            return {
                "status": 400,
                "message": "Invalid Token. Please provide a valid token"
            }, 400

        return f(current_user, *args, **kwargs)
    return wrapper


def get_auth_identity():
    """
        Returns the identity of the user accessing a protected
        endpoint.
    """
    return current_user


def save_raw_payload(undecoded, usr):
    """
        Receives and saves current user identity and encoded token payload.
    """
    global raw_auth, current_user
    raw_auth = undecoded
    current_user = usr


def get_raw_auth():
    """
        Returns the identity of the payload that logged this session.
    """
    return raw_auth
