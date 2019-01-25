import unittest
from app import create_app, db_instance
import json
from flask import current_app


class BaseTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app('testing')
        self.app.app_context().push()

        self.client = self.app.test_client()

        with self.app.app_context():
            db_instance.init_db()

        # create new user
        self.user_data = json.dumps(dict(
            username="DomesticableCow",
            email="cow@mammals.milkable",
            firstname="firstname",
            lastname="last",
            phonenumber=788488,
            othername="other",
            password="pa55word"))

        response = self.client.post('/api/v1/auth/register',
                                    data=self.user_data,
                                    content_type='application/json')
        self.new_user = json.loads(response.data.decode())

        login_response = self.client.post('/api/v1/auth/login',
                                          data=json.dumps(dict(
                                              username="DomesticableCow",
                                              email="cow@mammals.milkable",
                                              password="pa55word"
                                          )),
                                          content_type='application/json')
        user = login_response.get_json().get('data')[0].get('token')
        self.auth_header = {"Authorization": "Bearer " + user}

        # Register admin user
        user_data = json.dumps(dict(
            username="DomesticableAdmin",
            email="admin@mammals.milkable",
            password="pa55word",
            firstname="firstname",
            lastname="last",
            phonenumber=788488,
            othername="other",
            isadmin=True))

        self.client.post('api/v1/auth/register',
                         data=user_data,
                         content_type='application/json')

        # Login Admin

        user_res = self.client.post('api/v1/auth/login',
                                    data=json.dumps(dict(
                                        username="DomesticableAdmin",
                                        email="admin@mammals.milkable",
                                        password="pa55word"
                                    )),
                                    content_type='application/json')
        # Get Authorization token

        userH = user_res.get_json().get('data')[0].get('token')
        self.admin_auth = {"Authorization": "Bearer " + userH}

        self.client.post('api/v1/meetups',
                         content_type='application/json',
                         data=json.dumps(dict(
                             topic="Meats can Happen",
                             location="Over Here",
                             tags=['jump', 'eat', 'wake'],
                             happeningOn='2019-09-09T20:00:00'
                         )),
                         headers=self.admin_auth)

        # Create Question

        new_question = json.dumps(dict(
            title="One Other Question",
            body="This looks lik a body"))

        response = self.client.post('api/v1/meetups/1/questions',
                                    data=new_question,
                                    content_type='application/json',
                                    headers=self.auth_header)
        self.qcomment = json.dumps(dict(
            body="The cookies should come with milk too"))
        self.rsvp_y = json.dumps(dict(
            response="yes"
        ))
        self.rsvp_n = json.dumps(dict(
            response="no"
        ))
        self.rsvp_f = json.dumps(dict(
            response="so"
        ))

    def post(self, path, data=None, headers=None):

        if not headers:
            headers = self.auth_header
        res = self.client.post(path,
                               data=data,
                               content_type='application/json',
                               headers=headers)
        return res

    def get(self, path, headers=None):
        if not headers:
            headers = self.admin_auth
        res = self.client.get(path,
                              content_type='application/json',
                              headers=headers)
        return res

    def teardown(self):
        db_instance.drop_tables()
