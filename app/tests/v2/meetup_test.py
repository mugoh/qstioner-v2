from .base_test import BaseTestCase
import json


class MeetUpTests(BaseTestCase):

    def test_create_meetup_as_non_admin(self):
        response = self.client.post('api/v1/meetups',
                                    data=json.dumps(dict(
                                        topic="Meats can Happen",
                                        location="Over Somewhere",
                                        happeningOn="2019-01-01T00:10:00",
                                        tags=['jump', 'eat', 'woke']
                                    )),
                                    content_type='application/json',
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 403,
                         msg="Fails to create new meetup")

    def test_get_all_meetups(self):
        response = self.client.get('api/v1/meetups/upcoming',
                                   content_type='application/json',
                                   headers=self.auth_header)
        self.assertEqual(response.status_code, 200)

    def test_create_new_meetup_twice(self):
        user_data = json.dumps(dict(
            username="DomesticableAdmin",
            email="admin@mammals.milkable",
            password="pa55word",
            isAdmin=True))

        # Register admin user

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

        # Having happeningOn paramenter here gets cocky.
        res = self.client.post('api/v1/meetups',
                               content_type='application/json',
                               data=json.dumps(dict(
                                   topic="Meats can Happen",
                                   location="Over Here",
                                   tags=['jump', 'eat', 'wake']
                               )),
                               headers=self.admin_auth)
        self.assertEqual(res.status_code, 409,
                         msg="Fails. Creates an \
                         already existing meetup record")

    def test_get_individual_meetup(self):
        response = self.client.get('api/v1/meetups/4',
                                   content_type='application/json',
                                   headers=self.auth_header)
        print(response.data.decode())
        self.assertEqual(response.status_code, 404)

    def test_get_meetup_with_bad_auth_header(self):
        response = self.client.get('api/v1/meetups/4',
                                   content_type='application/json',
                                   headers={"Authorization": "Bearer "})
        print(response.data.decode())
        self.assertEqual(response.status_code, 400)

    def test_create_new_meetup(self):
        res = self.client.post('api/v1/meetups',
                               content_type='application/json',
                               data=json.dumps(dict(
                                   topic="Meats can Happen",
                                   location="Over Here",
                                   tags=['jump', 'eat', 'wake'],
                                   happeningOn='2019-09-09T20:00:00'
                               )),
                               headers=self.admin_auth)
        self.assertEqual(res.status_code, 409)

    def test_delete_missing_meetup(self):
        res = self.client.delete('api/v1/meetups/6',
                                 content_type='application/json',
                                 headers=self.admin_auth)
        self.assertEqual(res.status_code, 404)

    def test_delete_missing_meetup_with_bad_auth_header(self):
        res = self.client.delete('api/v1/meetups/6',
                                 content_type='application/json',
                                 headers={"Authorization": "Bearer "})
        self.assertEqual(res.status_code, 400)

    def test_delete_missing_meetup__bad_auth_header(self):
        res = self.client.delete('api/v1/meetups/6',
                                 content_type='application/json',
                                 headers={"Authorization": "Bearer"})
        self.assertEqual(res.status_code, 400)

    def test_delete_missing_meetup__bad_auth_payload(self):
        res = self.client.delete('api/v1/meetups/6',
                                 content_type='application/json',
                                 headers={"Authorization": "Bearer bad"})
        self.assertEqual(res.status_code, 400)

    def test_delete_meetup(self):

        self.client.post('api/v1/meetups',
                         content_type='application/json',
                         data=json.dumps(dict(
                             topic="Meats can Happen",
                             location="Over Here",
                             tags=['jump', 'eat', 'wake'],
                             happeningOn='2019-09-09T20:00:00'
                         )),
                         headers=self.admin_auth)

        res = self.client.delete('api/v1/meetups/1',
                                 content_type='application/json',
                                 headers=self.admin_auth)
        self.assertEqual(res.status_code, 200)

    def test_create_meetup_with_invalid_date(self):
        res = self.client.post('api/v1/meetups',
                               content_type='application/json',
                               data=json.dumps(dict(
                                   topic="Meats can Happen",
                                   location="Over Here",
                                   tags=['jump', 'eat', 'wake'],
                                   happeningOn='2019-08-08 20'
                               )),
                               headers=self.admin_auth)
        self.assertEqual(res.status_code, 400)
