"""
    This module contains test that verify uploads
    of images to a meetup.
"""

from .base_test import BaseTestCase
import io


class ImageUploadTest(BaseTestCase):

    def test_upload_image_to_meetup(self):
        # Use StringIO to simulate file object

        data = {
            'image': (io.BytesIO(b'my file contents'), 'test_file.png'),
        }

        expected_response = 'Upload Successful'

        res = self.client.post('api/v1/meetups/1/images',
                               data=data,
                               content_type='multipart/form-data',
                               headers=self.auth_header)

        self.assertEqual(expected_response, res.get_json().get('message'),
                         msg="Fails to allow user to post images to meetup")

    def test_upload_image_to_missing_meetup(self):

        data = {
            'image': (io.BytesIO(b'Might be a file'), 'image.png'),
        }

        res = self.client.post('api/v1/meetups/404/images',
                               data=data,
                               content_type='multipart/form-data',
                               headers=self.auth_header)

        self.assertEqual(res.get_json().get('message'),
                         'Meetup of ID 404 non-existent',
                         "Fails. Uploads image to missing meetup")
