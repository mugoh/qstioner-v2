from .base_test import BaseTestCase
import json


class RSVPTest(BaseTestCase):

    def test_create_new_rsvp(self):

        response = self.post('api/v1/meetups/1/response',
                             data=self.rsvp_y)

        self.assertEqual(response.status_code, 201,
                         msg="Fails to rsvp for a meetup")

    def test_create_rsvp_with_unknown_response(self):
        # Known responses are 'yes', 'no' and 'maybe'

        response = self.post('api/v1/meetups/1/response',
                             data=self.rsvp_f)
        self.assertTrue("Your response is not known"
                        in response.get_json().get("message"),
                        msg="Fails to not\
                         create an rsvp with an invalid response")

    def test_rsvp_for_nonexistent_meetup(self):
        res = self.post('api/v1/meetups/500/response',
                        data=self.rsvp_y)

        res_msg = res.get_json().get('message')

        self.assertEqual(res_msg, "That meetup does not exist",
                         msg="Fails to not rsvp a missing meetup")

    def test_create_same_rsvp_more_than_once(self):

        self.post('api/v1/meetups/1/response',
                  data=self.rsvp_y)
        response = self.post('api/v1/meetups/1/response',
                             data=self.rsvp_y)

        self.assertEqual(response.status_code, 409,
                         msg="Fails. Allows user to create same rsvp twice")

    def test_fetch_rsvp_for_user(self):

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
        admin_auth = {"Authorization": "Bearer " + userH}

        response = self.get('api/v1/meetups/2/rsvp', headers=self.auth_header)

        self.assertEqual(response.status_code, 200,
                         msg="Fails to show a user Rsvp-ed meetups")

    def test_fetch_rsvp_for_as_non_current_user(self):

        response = self.get('api/v1/meetups/7/rsvp')

        self.assertEqual(response.status_code, 404,
                         msg="Fails to check current user when fetching rsvps")

    def test_fetch_rsvp_for_user_name(self):

        response = self.get('api/v1/meetups/DomesticableAdmin/rsvp')

        self.assertEqual(response.status_code, 200,
                         msg="Fails to show a user Rsvp-ed meetups")

    def test_fetch_rsvp_for_non_present_user_name(self):

        response = self.get('api/v1/meetups/DomesticableNon Admin/rsvp')

        self.assertEqual(response.status_code, 404,
                         msg="Fails allows unknow users\
                         to see rsvps for others")

    def test_fetch_rsvp_for_user_none_parameters(self):

        response = self.get('api/v1/meetups/''/rsvp')

        self.assertEqual(response.get_json(), None,
                         msg="Fails to show a user error for invalid args")
