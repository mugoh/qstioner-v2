"""
    This module contains the view for the comment resource
"""

from flask_restful import Resource, reqparse, inputs

from ..models.users import UserModel
from ..models.questions import QuestionModel
from ..models.comments import CommentModel
from ..utils.auth import auth_required


class Comments(Resource):
    """
    Allows a user to create a new comment and
    supports performing of requests on multiple
    existing comments.
    """

    @auth_required
    def post(this_user, self, id):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)

        parser.add_argument('body', required=True,
                            type=inputs.regex('^[A-Za-z0-9_ ]+$'),
                            help="Is that readable? Provide a valid comment")

        args = parser.parse_args(strict=True)

        # Find question by given ID
        if not QuestionModel.get_by_id(id):
            return {
                "Status": 404,
                "Message": f"Question of ID {id} non-existent"
            }, 404

        # Get id of current user
        user_id = UserModel.get_by_name(this_user, key_values=True).get('id')

        args.update(
            {"user": user_id,
             "question": id}
        )

        new_comment = CommentModel(**args)
        if not CommentModel.verify_unique(new_comment):
            data = new_comment.save()
        else:
            return {
                "Status": 409,
                "Message": "Looks like You have posted this comment before"
            }, 409

        return {
            "Status": 201,
            "Data": [CommentModel.zipToDict(keys, data, single=True)]
        }, 201


keys = ["id", "question", "user_id"
        "body"]
