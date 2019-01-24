"""
    This module containes all Question resources.Question.
"""
from flask_restful import Resource, reqparse, inputs
from flasgger import swag_from

from ..models.questions import QuestionModel
from ..models.users import UserModel
from ..models.meetups import MeetUpModel
from ..utils.auth import auth_required, get_auth_identity

from ..database.queries import (
    GET_ALL_QUESTIONS, DELETE_QUESTION, UPDATE_QUESTION)


class Questions(Resource):
    """
        A resource that allows a user to create a
        new questions and perform requests on multiple
        existing questions.
    """
    decorators = [auth_required]

    @swag_from('docs/question_post.yml')
    def post(this_user, self, meetup_id):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)

        parser.add_argument('title',
                            type=inputs.regex('^[A-Za-z0-9_ ?/.,"\\\':;]+$'),
                            required=True,
                            help="Title is blank or contains" +
                            "invalid characters")
        parser.add_argument('body',
                            type=inputs.regex('^[A-Za-z0-9_ ?/.,"\\\':;]+$'),
                            required=True,
                            help="Comment Body is blank or" +
                            "contains invalid characters")

        args = parser.parse_args(strict=True)

        # Add user to question record
        user = UserModel.get_by_name(get_auth_identity())
        if user:
            args.update({
                "user": user.username,
                "meetup": meetup_id
            })

        # Verify meetup to be added to question record

        if not MeetUpModel.get_by_id(meetup_id):
            return {
                "Status": 404,
                "Message": f"Meetup id {meetup_id} non-existent." +
                "Maybe create it?"
            }, 404

        new_questn = QuestionModel(**args)

        if not QuestionModel.verify_existence(new_questn):
            values = new_questn.save()
        else:
            return {
                "Status": 409,
                "Message": "Chill up. That question is already created"
            }, 409

        return {
            "Status": 201,
            "Data": QuestionModel.zipToDict(keys, values, single=True)
        }, 201

    @swag_from('docs/questions_get.yml')
    def get(this_user, self):
        """
            Returns all existing questions
        """
        data = QuestionModel.get_all(GET_ALL_QUESTIONS)

        if data:
            data = QuestionModel.zipToDict(keys, data)
        return {
            "Status": 200,
            "Data": data
        }, 200


class Question(Resource):
    """
        Performs requests on a single question
    """
    decorators = [auth_required]

    @swag_from('docs/question_get.yml')
    def get(this_user, self, id):
        """
            Retrieves an individual question
        """
        if not QuestionModel.get_by_id(id):
            return {
                "Status": 404,
                "Message": "That question does not exist. Wanna create it?"
            }, 404

        return {
            "Status": 200,
            "Data": [QuestionModel.get_by_id(id)]
        }, 200

    @swag_from('docs/question_put.yml')
    def put(this_user, self, id):
        """
            This endpoint allows a user to make changes to the
            of an existing comment.
        """
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)

        parser.add_argument('title', type=str)
        parser.add_argument('body', type=str)

        args = parser.parse_args(strict=True)

        question = QuestionModel.get_by_id(id, obj=True)

        if not question:
            return {
                "Status": 404,
                "Message": f"That question [ID {id}] does not exist. Maybe create it?"
            }, 404

        # Get the question dictionary data
        quesion_dict = QuestionModel.get_by_id(id)

        # Get non-None Arguments from the PUT request
        quesion_dict.update({key: value for key, value
                             in args.items() if value})

        # Update the old data with added new data
        details_to_post = {"title": quesion_dict.get('title'),
                           "body": quesion_dict.get("body"),
                           "id": quesion_dict.get("id")}

        question.update(UPDATE_QUESTION, tuple(details_to_post.values()))

        return {
            "Status": 200,
            "Message": "Question Updated",
            "Data": [QuestionModel.get_by_id(id)]
        }, 200

    @swag_from('docs/question_delete.yml')
    def delete(this_user, self, id):
        question = QuestionModel.get_by_id(id, obj=True)
        if not question:
            return {
                "Status": 404,
                "Error": "Question not existent"
            }, 404
        else:
            question.delete(DELETE_QUESTION, (id,))

            return {
                "Status": 200,
                "Message": f'Question of ID {id} deleted'
            }, 200


class QuestionVote(Resource):
    """
        Upvotes or downvotes an existing question.
    """
    @auth_required
    @swag_from('docs/question_vote.yml')
    def patch(this_user, self, id, vote):

        # Verify existence of given question id
        if not QuestionModel.get_by_id(id):
            return {
                "Status": 404,
                "Message": "That question does not exist. Wanna create it?"
            }, 404
        else:
            question = QuestionModel.get_by_id(id, obj=True)
        _user_id = UserModel.get_by_name(
            this_user, key_values=True).get('id')

        if vote == 'upvote':
            voted_question = question.update_votes(id, _user_id)
        elif vote == 'downvote':
            voted_question = question.update_votes(id, _user_id, add=False)

        # Handle unknown url str parameter
        else:
            return {
                "Status": 400,
                "Message": "Please, 'upvote' or 'downvote' only. Cool?"
            }, 400

        return {
            "Status": 200,
            "Data": [voted_question]
        }, 200


keys = ["id", "title", "body",
        "meetup", "user", "votes", "created_at"]
