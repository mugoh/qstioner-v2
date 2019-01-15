from flask_restful import Resource, reqparse
from flasgger import swag_from
import datetime

from ..models.meetups import MeetUpModel
from ..utils.auth import admin_required, auth_required, current_user_only
from ..utils.helpers import validate_date


class Meetups(Resource):
    """
        This resource allows an admin user to create a meetup.
        It also makes it possible for any user to fetch all existing meetups
    """
    @auth_required
    @admin_required
    @swag_from('docs/meetup_post.yml')
    def post(this_user, self):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)
        parser.add_argument('topic', type=str, required=True)
        parser.add_argument(
            'happeningOn', type=validate_date,
            default=datetime.datetime.utcnow().isoformat())
        parser.add_argument('tags', type=str, action='append')
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('images', type=str, action='append')

        args = parser.parse_args(strict=True)

        # Ensure a meetup isn't created with same data twice

        new_meetup = MeetUpModel(**args)

        if MeetUpModel.verify_unique(new_meetup):
            return {
                "Status": 409,
                "Message": "Relax, Meetup already created"
            }, 409

        new_meetup.save()

        return {
            "Status": 201,
            "Data": [new_meetup.dictify()]
        }, 201


class MeetUp(Resource):
    """
        This resource fetches all existing meetup records
    """
    @auth_required
    @swag_from('docs/meetups_get.yml')
    def get(this_user, self):

        return {
            "Status": 200,
            "Data": [MeetUpModel.get_all_meetups()]
        }, 200


class MeetUpItem(Resource):
    """
        Searches for a meetup by its id
        and returns a matching record.
    """
    @auth_required
    @swag_from('docs/meetup_get.yml')
    def get(this_user, self, id):

        if not MeetUpModel.get_by_id(id):
            return {
                "Status": 404,
                "Error": "Meetup non-existent"
            }, 404
        return {
            "Status": 200,
            "Data": [MeetUpModel.get_by_id(id)]
        }, 200

    @auth_required
    @swag_from('docs/meetup_delete.yml')
    def delete(this_user, self, id):
        meetup = MeetUpModel.get_by_id(id, obj=True)
        if not meetup:
            return {
                "Status": 404,
                "Error": "Meetup non-existent"
            }, 404
        else:
            meetup.delete()
        return {
            "Status": 200,
            "Message": "MeetUp deleted"
        }, 200
