"""
    This module contains resource views for the
    rsvp Resource
"""

from flask_restful import Resource
from flasgger import swag_from

from ..models.rsvp import RsvpModel
from ..models.meetups import MeetUpModel
from ..models.users import UserModel
from ..utils.auth import current_user_only, auth_required, get_auth_identity


class Rsvps(Resource):

    @auth_required
    @swag_from('docs/rsvp_post.yml')
    def post(this_user, self, id, response):
        """
            Creates an rsvp with refrence to a meetup and the
            existing user's
        """

        args = {}

        # Confirm response is valid

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

        user = UserModel.get_by_name(get_auth_identity())

        user_id = getattr(user, 'id')

        args.update({
            "user": user_id,
            "meetup": id,
            "response": response
        })

        # Create rsvp and confirm it's not a duplicate

        rsvp = RsvpModel(**args)
        if not RsvpModel.verify_unique(rsvp):
            rsvp.save()

        else:
            return {
                "Status": 409,
                "Message": "You've done that same rsvp already"
            }, 409

        return {
            "Status": 201,
            "Data": rsvp.dictify()
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

        # Find none 'None' ulr

        query_parameter = next((item for item in [id, username]
                                if item is not None), None)

        # Get user id
        # Rsvp stores user by id
        if username and UserModel.get_by_name(username):
            query_parameter = UserModel.get_by_name(username).id

        rsvps = RsvpModel.get_all_rsvps(obj=True)

        users_rsvps = [rsvp for rsvp in rsvps
                       if getattr(rsvp, 'user') == query_parameter]

        # Find all these rsvp-ed meetups
        meetups = [item.id for item in users_rsvps]
        meetups_data = list(map(lambda x: MeetUpModel.get_by_id(x), meetups))

        return {"Status": 200,
                "Data": [(id + 1, data) for id, data
                         in enumerate(meetups_data)]}, 200
