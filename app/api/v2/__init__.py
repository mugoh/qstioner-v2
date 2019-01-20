from flask_restful import Api
from flask import Blueprint

from ...api.v2.views.user import UsersRegistration, UserLogin, UserLogout
from ...api.v2.views.meetups import (
    Meetups, MeetUp, MeetUpItem, MeetupImage, MeetUpTags, MeetUpTag)
from ...api.v2.views.questions import Question, Questions, QuestionVote
from ...api.v2.views.rsvp import Rsvps, Rsvp
from .views.comments import Comments, CommentsUser

auth_blueprint = Blueprint("auth", __name__, url_prefix='/api/v1/auth/')
app_blueprint = Blueprint("app", __name__, url_prefix='/api/v1/')

auth_api = Api(auth_blueprint)
app_api = Api(app_blueprint)

auth_api.add_resource(UsersRegistration, 'register')
auth_api.add_resource(UserLogin, 'login')
auth_api.add_resource(UserLogout, 'logout')

app_api.add_resource(Meetups, 'meetups')
app_api.add_resource(MeetUp, 'meetups/upcoming')
app_api.add_resource(MeetUpItem, 'meetups/<int:id>')
app_api.add_resource(MeetupImage, 'meetups/<int:id>/images')
app_api.add_resource(MeetUpTags, 'meetup/<int:meetup_id>/<tag>')
app_api.add_resource(MeetUpTag, 'meetup/<tag>')

app_api.add_resource(Questions, 'questions')
app_api.add_resource(Question, 'questions/<int:id>')
app_api.add_resource(QuestionVote, 'questions/<int:id>/<vote>',
                     methods=['PATCH'])
app_api.add_resource(Rsvps, 'meetups/<int:id>/<response>')
app_api.add_resource(Rsvp, 'meetups/<int:id>/rsvp', 'meetups/<username>/rsvp')


app_api.add_resource(Comments, 'questions/<int:id>/comment')
app_api.add_resource(CommentsUser, 'questions/<int:id>/<username>/comment',
                     'questions/<int:id>/<int:usr_id>/comment')
