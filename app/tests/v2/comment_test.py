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

    def test_create_comment_for_missing_question(self):
        res = self.post('api/v1/questions/404/comment',
                        data=self.qcomment)
        self.assertTrue('non-existent' in res.get_json().get('Message'),
                        msg="Fails. Posts comment to missing question")
