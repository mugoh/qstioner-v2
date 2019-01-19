from .base_test import BaseTestCase


class CommentTest(BaseTestCase):

    def test_get_comments_for_empty_table(self):
        res = self.get('api/v1/questions/1/comment')

        print(res.get_json())

        self.assertEqual(res.get_json().get('Data'),
                         [],
                         msg="Fails. Initiliazes comments table with data")
