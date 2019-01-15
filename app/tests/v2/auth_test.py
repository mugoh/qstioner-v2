from .base_test import BaseTestCase
import json
from flask import jsonify


class AuthTestCases(BaseTestCase):
    """
    Tests user authentication

    """

    def test_get_registered_users(self):
        response = self.client.get('/api/v1/auth/register',
                                   data=self.user_data,
                                   content_type='application/json')
        res = json.loads(response.data.decode()).get("Data")

        self.assertTrue(isinstance(res, list),
                        msg="Fails to return user records as list")

        self.assertEqual(response.status_code, 200)

    def test_register_already_registered_user(self):

        response = self.client.post('/api/v1/auth/register',
                                    data=self.user_data,
                                    content_type='application/json')
        res = json.loads(response.data.decode()).get('Message')

        res_msg = "Account exists. Maybe log in?"
        self.assertEqual(res,
                         res_msg,
                         msg="Fails to registration of existing account")

    def test_register_with_invalid_email(self):
        user_data = json.dumps(dict(
            username="DomesticableCow",
            email="cow@mammals",
            password="pa55word"))

        response = self.client.post('/api/v1/auth/register',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 400,
                        msg="Fails. Registers user with invalid email")

    def test_register_with_existing_username(self):
        user_data = json.dumps(dict(
            username="DomesticableCow",
            email="cow@mammals.new",
            password="pa55word"))

        response = self.client.post('/api/v1/auth/register',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 409,
                        msg="Fails. Registers user with existing username")

    def test_register_with_invalid_password(self):
        user_data = json.dumps(dict(
            username="DomesticableCow",
            email="cow@mammals.milkable",
            password="pass"))

        response = self.client.post('/api/v1/auth/register',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 400,
                        msg="Fails. Registers user with password\
                        of length less than six characters")

    def test_register_with_invalid_usrname(self):
        user_data = json.dumps(dict(
            username="Domesticable Cow",
            email="cow@mammals.milkable",
            password="pass"))

        response = self.client.post('/api/v1/auth/register',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 400,
                        msg="Fails. Allows user \
                        to register with invalid user name")

    def test_register_with_digits_usrname(self):
        user_data = json.dumps(dict(
            username="Domesticable45Cow",
            email="cow@mammals.milkable",
            password="pass"))

        response = self.client.post('/api/v1/auth/register',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 400,
                        msg="Fails. Allows user \
                        to register with invalid user name")

    def test_send_request_with_invalid_json(self):
        response = self.client.post('/api/v1/auth/register',
                                    data=self.user_data,
                                    )
        res = json.loads(response.data.decode())
        print(res)

        # self.assertEqual(res, res_msg,
        #                 msg="Fails to validate json headers")

        self.assertEqual(response.status_code, 400)

    def test_login_registered_user(self):
        response = self.client.post('/api/v1/auth/login',
                                    data=self.user_data,
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200,
                         msg="Fails to login registered user")

    def test_login_with_invalid_email(self):
        user_data = json.dumps(dict(
            username="DomesticableCow",
            email="cow@mammals",
            password="pa55word"))

        response = self.client.post('/api/v1/auth/login',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 400,
                        msg="Fails. Logs in user with invalid email")

    def test_login_with_incorrect_password(self):
        user_data = json.dumps(dict(
            username="DomesticableCow",
            email="cow@mammals.milkable",
            password="password"))

        response = self.client.post('/api/v1/auth/login',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 403,
                        msg="Fails. Logs in user with invalid password")

    def test_login_with_unregistered_email(self):
        user_data = json.dumps(dict(
            username="DomesticableCow",
            email="cow@mammals.alien",
            password="pa55word"))

        response = self.client.post('/api/v1/auth/login',
                                    data=user_data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404,
                         msg="Fails. Logs in user with unknown email")

    def test_logged_in_user_can_log_out(self):

        self.client.post('/api/v1/auth/login',
                         data=self.user_data,
                         content_type='application/json')

        response = self.client.delete('/api/v1/auth/logout',
                                      headers=self.auth_header,
                                      data=self.user_data,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200,
                         msg="Fails to logout user")
