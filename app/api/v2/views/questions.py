"""
    This module containes all Question resources.Question.
"""
from flask_restful import Resource, reqparse
from flasgger import swag_from

from ..models.questions import QuestionModel
from ..models.users import UserModel
from ..models.meetups import MeetUpModel
from ..utils.auth import auth_required, get_auth_identity


class Questions(Resource):
    """
        A resource that allows a suser to create a
        new questions and perform requests on existing
        multiple questions.
    """
    decorators = [auth_required]

    @swag_from('docs/question_post.yml')
    def post(this_user, self):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)

        parser.add_argument('title', type=str, required=True)
        parser.add_argument('body', type=str, required=True)
        parser.add_argument('meetup', type=int, default=1)

        args = parser.parse_args(strict=True)

        # Add user to question record
        user = UserModel.get_by_name(get_auth_identity())
        if user:
            args.update({
                "user": user.id
            })

        # Verify meetup to be added to question record

        if not MeetUpModel.get_by_id(args['meetup']):
            return {
                "Status": 404,
                "Message": "Meetup id non-existent. Maybe create it?"
            }, 404

        new_questn = QuestionModel(**args)

        if not QuestionModel.verify_existence(new_questn):
            new_questn.save()

        else:
            return {
                "Status": 409,
                "Message": "Chill up. That question is already created"
            }, 409

        return {
            "Status": 201,
            "Data": [new_questn.dictify()]
        }, 201

    @swag_from('docs/questions_get.yml')
    def get(this_user, self):
        """
            Returns all exsisting questions
        """

        return {
            "Status": 200,
            "Data": [QuestionModel.get_all_questions()]
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

    @swag_from('docs/question_delete.yml')
    def delete(this_user, id):
        pass


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

        if vote == 'upvote':
            question.update_votes()
        elif vote == 'downvote':
            question.update_votes(add=False)

        # Handle unknown url str parameter
        else:
            return {
                "Status": 400,
                "Message": "Please, 'upvote' or 'downvote' only. Cool?"
            }, 400

        return {
            "Status": 200,
            "Data": [question.dictify()]
        }, 200
