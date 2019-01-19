import json

from .base_test import BaseTestCase


class CommentTest(BaseTestCase):

    def test_get_comments_for_empty_table(self):
        res = self.get('api/v1/questions/1/comment')

        self.assertEqual(res.get_json().get('Data'),
                         [],
                         msg="Fails. Initiliazes comments table with data")

    def test_get_comments_for_missing_question(self):
        res = self.get('api/v1/questions/404/comment')

        expected_response = 'Question of ID 404 non-existent'
        self.assertTrue(
            expected_response
            in res.get_json().get('Message'),
            msg="Fails. Allows user to get comments of non-existent question")

    def test_create_comment_for_question(self):
        data = json.dumps(dict(
            body="I'll be there for the cookies"
        ))

        res = self.post('api/v1/questions/1/comment',
                        data=data)

        self.assertEqual(res.get_json().get('Data')[0].get('body'),
                         "I'll be there for the cookies",
                         msg="Fails to create  comment")

    """def test_create_comment_for_missing_question(self):
        res = self.post('api/v1/questions/404/comment',
                        data=self.qcomment)
        self.assertTrue('non-existent' in res.get_json().get('Message'),
                        msg="Fails. Posts comment to missing question")

    def test_posted_comment_exists_in_record(self):
        self.post('api/v1/questions/1/comment',
                  data=self.qcomment)

        res = self.get('api/v1/questions/1/comment')

        self.assertNotEqual(res.get_json().get('Data'),
                            [],
                            msg="Fails to store posted comment\
                            in comments table")

    def test_post_same_comment_twice(self):
        self.post('api/v1/questions/1/comment',
                  data=self.qcomment)
        res = self.post('api/v1/questions/1/comment',
                        data=self.qcomment)

        self.assertEqual('Looks like You have posted this comment before',
                         res.get_json().get('Message'),
                         "Fails. Allows a user to re-post the same comment")

    def test_retirieve_comments_for_user(self):
        res = self.get('api/v1/questions/1/2/comment')
        self.assertEqual(res.get_json().get('Data'),
                         [],
                         msg="Fails to retrieve comments for user")

    def test_retirieve_user_comments_for_missing_question(self):
        res = self.get('api/v1/questions/404/2/comment')
        self.assertTrue('non-existent' in res.get_json().get('Message'),
                        msg="Fails. Allows user to fetch comments for questions\
                        not present")"""

    def test_post_comment_then_fetch_for_user(self):

        # Post comment
        self.post('api/v1/questions/1/comment',
                  data=self.qcomment,
                  headers=self.auth_header)

        # Get comments with this user's ID
        res = self.get('api/v1/questions/1/1/comment',
                       headers=self.auth_header)

        self.assertEqual(res.get_json().get('Data')[0].get('user_id'),
                         1,
                         msg="Fails to fetch comments  posted by current user")
