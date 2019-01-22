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
                        not present")

    def test_post_comment_then_fetch_by_user_id(self):

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

    def test_retrieve_comments_by_username(self):
        res = self.get('api/v1/questions/1/DomesticableAdmin/comment')
        print(res.get_json())
        self.assertEqual(res.get_json().get('Data'),
                         [],
                         msg="Fails to retrieve comments for user")

    def test_edit_missing_user_comments(self):
        data = json.dumps(dict(
            body="I'll be there for the cookies"
        ))
        res = self.client.put('api/v1/comments/1',
                              data=data,
                              headers=self.auth_header,
                              content_type='application/json')
        self.assertTrue('not posted any' in
                        res.get_json().get('Message'),
                        "Fails. Allows user to edit they did not post")

    def test_edit_comment(self):
        data = json.dumps(dict(
            body="I'll be there for the cookies"
        ))
        res = self.post('api/v1/questions/1/comment',
                        data=data)

        res = self.client.put('api/v1/comments/1',
                              data=data,
                              headers=self.auth_header,
                              content_type='application/json')

        self.assertEqual('Comment Updated',
                         res.get_json().get('Message'),
                         "Fails to edit user quesiton")

    def test_edit_comment_with_missing_id(self):
        data = json.dumps(dict(
            body="I'll be there for the cookies"
        ))
        res = self.post('api/v1/questions/1/comment',
                        data=data)

        res = self.client.put('api/v1/comments/404',
                              data=data,
                              headers=self.auth_header,
                              content_type='application/json')

        self.assertEqual('Comment of ID 404 missing',
                         res.get_json().get('Message'),
                         "Fails to edit user quesiton")

    def test_delete_comment(self):
        data = json.dumps(dict(
            body="I'll be there for the cookies"
        ))
        self.post('api/v1/questions/1/comment',
                  data=data)
        res = self.client.delete('api/v1/comments/1',
                                 headers=self.auth_header)
        print(res.get_json())

        self.assertEqual(res.get_json().get('Message'),
                         "Comment of ID 1 deleted",
                         "Fails to delete a user comment")

    def test_delete_missing_comment(self):

        res = self.client.delete('api/v1/comments/1',
                                 headers=self.auth_header)
        print(res.get_json())

        self.assertEqual(res.get_json().get('Message'),
                         "Comment of ID 1 missing",
                         "Fails. Deletes missing user comment")
