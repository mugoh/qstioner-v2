"""
    This module contains the view for the comment resource
"""

from flask_restful import Resource, reqparse, inputs


class Comments(Resource):
    """
    Allows a user to create a new comment and
    supports performing of requests on multiple
    existing comments.
    """

    def post(self):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)

        parser.add_argument('body', required=True,
                            type=inputs.regex('^[A-Za-z0-9_ ]+$'),
                            help="Is that readable? Provide a valid comment")

        args = parser.parse_args(strict=True)
