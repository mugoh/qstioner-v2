from .base_test import BaseTestCase
from app.api.v1.models.questions import QuestionModel
import json


class TestQuestions(BaseTestCase):

    def test_create_new_question(self):
        self.new_question = json.dumps(dict(
            title="One Question",
            body="This looks lika a body",
            meetup=1))

        response = self.client.post('api/v1/questions',
                                    data=self.new_question,
                                    content_type='application/json',
                                    headers=self.auth_header)

        # Verify meetup refrenced exists

        response_confirm_meetup = self.client.get(
            'api/v1/meetups/1',
            content_type='application/json',
            headers=self.auth_header)

        self.assertEqual(response_confirm_meetup.status_code, 200,
                         msg="Fails to fetch meetup for question")

        self.assertEqual(response.status_code, 201,
                         msg="Fails to create a new question")

    def test_create_existing_question(self):
        new_question = json.dumps(dict(
            title="One Question Dup",
            body="This looks like a body"))

        self.client.post('api/v1/questions',
                         data=new_question,
                         content_type='application/json',
                         headers=self.auth_header)

        response = self.client.post('api/v1/questions',
                                    data=new_question,
                                    content_type='application/json',
                                    headers=self.auth_header)
        self.assertEqual(response.status_code, 409,
                         msg="Fails to not create\
                         a question with same data twice")

    def test_create_new_question_that_references_nonexistent_meetup(self):
        self.new_question = json.dumps(dict(
            title="One Question",
            body="This looks lika a body",
            meetup=400))

        response = self.client.post('api/v1/questions',
                                    data=self.new_question,
                                    content_type='application/json',
                                    headers=self.auth_header)
        response_confirm_meetup = self.client.get(
            'api/v1/meetups/400',
            content_type='application/json',
            headers=self.auth_header)

        self.assertEqual(response_confirm_meetup.status_code, 404,
                         msg="Fails to not create question\
                         for a non-existemt meetup")

        self.assertEqual(response.status_code, 404,
                         msg="Fails to not create question\
                         for a non-existemt meetup")

    def test_get_all_questions(self):

        response = self.client.get('api/v1/questions',
                                   content_type='application/json',
                                   headers=self.auth_header)
        self.assertEqual(response.status_code, 200,
                         msg="Fails to get all questions")

    def test_get_single_question(self):

        response = self.client.get('api/v1/questions/1',
                                   content_type='application/json',
                                   headers=self.auth_header)
        self.assertEqual(response.status_code, 200,
                         msg="Fails to fetch individual question")

    def test_get_non_existent_question(self):

        response = self.client.get('api/v1/questions/400',
                                   content_type='application/json',
                                   headers=self.auth_header)
        self.assertEqual(response.status_code, 404,
                         msg="Fails to return error\
                         on fetching missing question")

    def test_down_vote_question(self):
        res = self.client.patch('api/v1/questions/1/downvote',
                                content_type='application/json',
                                headers=self.auth_header)

        expected_votes = res.get_json().get('Data')[0].get('votes')

        self.assertEqual(expected_votes, -1,
                         msg="Fails to downvote a question")

    def test_up_vote_question(self):
        res = self.client.patch('api/v1/questions/1/upvote',
                                content_type='application/json',
                                headers=self.auth_header)

        expected_votes = res.get_json().get('Data')[0].get('votes')

        self.assertEqual(expected_votes, 0,
                         msg="Fails to upvote a question")

    def test_vote_non_existent_question(self):
        res = self.client.patch('api/v1/questions/500/upvote',
                                content_type='application/json',
                                headers=self.auth_header)

        self.assertEqual(res.status_code, 404,
                         msg="Fails. Votes a missing question")

    def test_vote_question_with_invalid_string(self):
        res = self.client.patch('api/v1/questions/1/invalid',
                                content_type='application/json',
                                headers=self.auth_header)

        self.assertEqual(res.status_code, 400,
                         msg="Fails to validate vote request")

    def test_change_vote_on_question_instance_directly(self):
        new_question = dict(
            title="One Question Again",
            body="This looks like  a semi-body",
            meetup=400
        )

        res = QuestionModel(**new_question)

        with self.assertRaises(AttributeError) as ctx:
            res.votes = 300
        self.assertTrue('Oops! You are not allowed to do that' in
                        str(ctx.exception))
