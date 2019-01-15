import unittest
from app import create_app
import json


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

        # create new user
        self.user_data = json.dumps(dict(
            username="DomesticableCow",
            email="cow@mammals.milkable",
            password="pa55word"))

        response = self.client.post('/api/v1/auth/register',
                                    data=self.user_data,
                                    content_type='application/json')
        self.new_user = json.loads(response.data.decode())

        login_response = self.client.post('/api/v1/auth/login',
                                          data=self.user_data,
                                          content_type='application/json')
        user = json.loads(login_response.data.decode()
                          ).get("Data")[0].get('token')
        self.auth_header = {"Authorization": "Bearer " + user.split("'")[1]}

        # Register admin user
        user_data = json.dumps(dict(
            username="DomesticableAdmin",
            email="admin@mammals.milkable",
            password="pa55word",
            isAdmin=True))
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

        userH = user_res.get_json().get('Data')[0].get('token')
        self.admin_auth = {"Authorization": "Bearer " + userH.split("'")[1]}

        self.client.post('api/v1/meetups',
                         content_type='application/json',
                         data=json.dumps(dict(
                             topic="Meats can Happen",
                             location="Over Here",
                             tags=['jump', 'eat', 'wake'],
                             happeningOn='2019-09-09T20:00:00'
                         )),
                         headers=self.admin_auth)

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
