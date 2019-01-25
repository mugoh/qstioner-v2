from .base_test import BaseTestCase
import json


class AuthTestCases(BaseTestCase):
    """
    Tests user authentication

    """

    def test_get_registered_users(self):
        """
            Verify endpoint for fetching all current users
            in the application.
        """
        response = self.client.get('/api/v1/auth/register',
                                   data=self.user_data,
                                   content_type='application/json')
        res = json.loads(response.data.decode()).get("data")

        self.assertTrue(isinstance(res, list),
                        msg="Fails to return user records as list")

        self.assertEqual(response.status_code, 200)

    def test_register_already_registered_user(self):
        """
            Verify a user's details cannot be reused in
            making another account.
        """

        response = self.client.post('/api/v1/auth/register',
                                    data=self.user_data,
                                    content_type='application/json')
        res = json.loads(response.data.decode()).get('message')

        res_msg = "Account exists. Maybe log in?"
        self.assertEqual(res,
                         res_msg,
                         msg="Fails to registration of existing account")

    def test_register_with_invalid_email(self):
        """
            Verify a user cannot register with an email pattern
            that's not accepted.
        """
        user_data = json.dumps(dict(
            username="DomesticableCow",
            email="cow@mammals",
            password="pa55word",
            firstname="name",
            lastname="name",
            phonenumber=7234))

        response = self.client.post('/api/v1/auth/register',
                                    data=user_data,
                                    content_type='application/json')

        self.assertTrue(response.status_code == 400,
                        msg="Fails. Registers user with invalid email")

    def test_register_with_existing_username(self):
        """
            Tests that accounts are created with unique
            usernames.
        """
        user_data = json.dumps(dict(
            username="DomesticableCow",
            email="cow@mammals.milk",
            password="pa55word",
            firstname="name",
            lastname="name",
            phonenumber=7234))

        response = self.client.post('/api/v1/auth/register',
                                    data=user_data,
                                    content_type='application/json')

        print(response.get_json())
        self.assertEqual(response.status_code, 409,
                         msg="Fails. Registers user with existing username")

    def test_register_with_invalid_password(self):
        """
            Verify password length is met before an account
            is created for a user with this password.
        """
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
        """
            Tests that the username pattern is met before attempting
            to register user with given username.
        """
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
        """
            Verifys rasising pf a ValueError when a registration
            with digits username is attempted.
        """
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
        """
            Tests an error response is raised when a post
            request is send without a valid content-type JSON header.
        """
        response = self.client.post('/api/v1/auth/register',
                                    data=self.user_data,
                                    )
        json.loads(response.data.decode())

        # self.assertEqual(res, res_msg,
        #                 msg="Fails to validate json headers")

        self.assertEqual(response.status_code, 400)

    def test_login_registered_user(self):
        """
            Tests a registered user can login and and have access to
            the aaplication features.
        """
        response = self.client.post('/api/v1/auth/login',
                                    data=json.dumps(dict(
                                        username="DomesticableCow",
                                        email="cow@mammals.milkable",
                                        password="pa55word")),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200,
                         msg="Fails to login registered user")

    def test_login_with_invalid_email(self):
        """
            Verifies that a email pattern that doesn't match
            a correct email format cannot be used in a login
            request.
        """
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
        """
            Verifies that a user given an access session
            logged in with a stored username and password.
        """
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
        """
            Tests an email not registered cannot be used in accessing
            an account on the application.
        """
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
        """
            Tests that a user with account access can
            log out of the system and render the account inaccessible
            until the next log in.
        """

        self.client.post('/api/v1/auth/login',
                         data=self.user_data,
                         content_type='application/json')

        response = self.client.delete('/api/v1/auth/logout',
                                      headers=self.auth_header,
                                      data=self.user_data,
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200,
                         msg="Fails to logout user")
