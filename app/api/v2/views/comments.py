"""
    This module contains the view for the comment resource
"""

from flask_restful import Resource, reqparse, inputs
from flasgger import swag_from

from ..models.users import UserModel
from ..models.questions import QuestionModel
from ..models.comments import CommentModel
from ..utils.auth import auth_required, current_user_only
from ..database.queries import (
    GET_ALL_COMMENTS, UPDATE_COMMENT, DELETE_COMMENT, GET_COMMENT_BY_ID)


class Comments(Resource):
    """
    Allows a user to create a new comment and
    supports performing of requests on multiple
    existing comments.
    """

    @auth_required
    @swag_from('docs/comments_post.yml')
    def post(this_user, self, id):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)

        parser.add_argument('body', required=True,
                            type=inputs.regex('^[A-Za-z0-9_ ?/!.,"\\\':;]+$'),
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

    @auth_required
    @swag_from('docs/comments_get.yml')
    def get(this_user, self, id):
        """
            Returns all existing comments to a question
        """

        # Find question from given ID

        if not QuestionModel.get_by_id(id):
            return {
                "Status": 404,
                "Message": f"Question of ID {id} non-existent"
            }, 404

        data = CommentModel.get_all(GET_ALL_COMMENTS, (id,))

        if data:
            data = CommentModel.zipToDict(keys, data)
        return {
            "Status": 200,
            "Data": data
        }, 200


class CommentsUser(Resource):
    """
        Handles requests to comments of a specific user
        on a meetup question
    """
    @auth_required
    @current_user_only
    @swag_from('docs/comments_get_user.yml')
    def get(this_user, self, id, username=None, usr_id=None):
        """
            Returns all existing comments to a question
        """

        # Find question from given ID

        if not QuestionModel.get_by_id(id):
            return {
                "Status": 404,
                "Message": f"Question of ID {id} non-existent"
            }, 404

        user_id = usr_id

        if username:
            user_id = UserModel.get_by_name(
                this_user, key_values=True).get('id')

        data = CommentModel.get_for_user(user_id)

        if data:
            data = CommentModel.zipToDict(keys, data)
        return {
            "Status": 200,
            "Data": data
        }, 200


class CommentUpdate(Resource):
    """
        This resource allows use of a PUT or DELETE request on
        an existing comment without having to specify
        the Question ID of the comment.
    """
    @auth_required
    @swag_from('docs/comment_put.yml')
    def put(this_user, self, id):
        """
            Updates a user comment
        """
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)

        parser.add_argument('body', required=True,
                            type=inputs.regex(
                                '^[A-Za-z0-9_ ?/!.,"\\\':;]+$'),
                            help="Is that readable? Provide a valid comment")

        args = parser.parse_args(strict=True)

        # Get the user ID of user sending request
        user = UserModel.get_by_name(this_user)
        user_id = getattr(user, 'id')

        # Find Comments posted by this USER
        data = CommentModel.get_for_user(user_id)

        if not data:

            return {
                "Status": 404,
                "Message": f'{this_user} has not posted any comment yet'
            }, 404
        args.update({"id": id})

        if not CommentModel.get_by_id(GET_COMMENT_BY_ID, (id,)):
            return {
                "Status": 404,
                "Message": f"Comment of ID {id} missing"
            }, 404

        user.update(UPDATE_COMMENT, tuple(args.values()))

        return {
            "Status": 200,
            "Message": "Comment Updated",
        }, 200

    @auth_required
    @swag_from('docs/comment_delete.yml')
    def delete(this_user, self, id):
        """
            Allows a user to delete a present comment
        """

        if not CommentModel.get_by_id(GET_COMMENT_BY_ID, (id,)):
            return {
                "Status": 404,
                "Message": f"Comment of ID {id} missing"
            }, 404

        user = UserModel.get_by_name(this_user)

        user.delete(DELETE_COMMENT, (id,))

        return {
            "Status": 200,
            "Message": f'Comment of ID {id} deleted'
        }, 200


keys = ["id", "question", "user_id",
        "body"]
