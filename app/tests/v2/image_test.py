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
            'image': (io.BytesIO(b'my file contents'), 'test_file.txt'),
        }

        expected_response = 'Upload Successful'

        res = self.client.post('api/v1/meetups/1/images',
                               data=data,
                               content_type='multipart/form-data')

        self.assertEqual(expected_response, res.get_json().get('Message'),
                         msg="Fails to allow user to post images to meetup")
