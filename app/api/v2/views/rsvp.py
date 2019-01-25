"""
    This module contains resource views for the
    rsvp Resource
"""

from flask_restful import Resource, reqparse, inputs
from flasgger import swag_from

from itertools import zip_longest

from ..models.rsvp import RsvpModel
from ..models.meetups import MeetUpModel
from ..models.users import UserModel
from ..utils.auth import current_user_only, auth_required, get_auth_identity


class Rsvps(Resource):

    @auth_required
    @swag_from('docs/rsvp_post.yml')
    def post(this_user, self, id):
        """
            Creates an rsvp with refrence to a meetup and the
            existing user's
        """

        parser = reqparse.RequestParser(trim=True, bundle_errors=True)

        parser.add_argument('response', required=True,
                            type=inputs.regex('^[A-Za-z]+$'),
                            help="Is that readable? Provide a valid rsvp")

        args = parser.parse_args(strict=True)

        # Confirm response is valid
        response = args.get('response')

        expected_responses = ['yes', 'no', 'maybe']

        err_msg = "Your response is not known. Make it: " + \
            str(expected_responses[:-1]) + ' or ' + str(expected_responses[-1])

        if response not in expected_responses:
            return {
                "Status": 400,
                "Message": err_msg
            }, 400

        # Confirm existence of the meetup  to rsvp

        if not MeetUpModel.get_by_id(id):
            return {
                "Status": 404,
                "Message": "That meetup does not exist"
            }, 404

        # Retrieve this user details in key, value pairs
        user = UserModel.get_by_name(get_auth_identity(), key_values=True)

        user_id = user.get('id')

        args.update({
            "user": user_id,
            "meetup": id,
            "response": response
        })

        # Create rsvp and confirm it's not a duplicate

        rsvp = RsvpModel(**args)
        if not RsvpModel.verify_unique(rsvp):
            data = rsvp.save()

        else:
            return {
                "Status": 409,
                "Message": "You've done that same rsvp already"
            }, 409

        return {
            "Status": 201,
            "Data": [RsvpModel.zipToDict(keys, data, single=True)]
        }, 201


class Rsvp(Resource):

    @auth_required
    @current_user_only
    @swag_from('docs/rsvps_user_get.yml')
    def get(this_user, self, id=None, username=None):
        """
            Allows the current user to see every existing
            meetups s/he has responded to an rsvp for
        """

        # Find none 'None' ulr. Remember a user passes either an
        # ID or a USERNAME. Use either that's not NONE.

        query_parameter = next((item for item in [id, username]
                                if item is not None), None)

        # If we got a USERNAME, Get this user's id
        # Why? Rsvp stores user by ID

        if username and UserModel.get_by_name(username):
            query_parameter = UserModel.get_by_name(username).id

        # Hold meetup ID's retrieved by query
        meetup_and_responses = RsvpModel.get_for_user(query_parameter)

        meetup_ids = [_id for _id, res in meetup_and_responses]
        responses = [res for _id, res in meetup_and_responses]

        # Find all these rsvp-ed meetups
        meetups_data = list(
            map(lambda x: MeetUpModel.get_by_id(x), meetup_ids))

        return {"Status": 200,
                "Data": [(response, meetup) for response, meetup
                         in zip_longest(
                             responses, meetups_data)]}, 200


keys = ["id", "meetup", "user_id",
        "response"]
