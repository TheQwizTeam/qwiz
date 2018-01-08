from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Tag, Question, Room, Contestant


class RestTagTests(APITestCase):
    """
    REST API Tag test cases.
    """
    def setUp(self):
        """
        Set up Tag tests
        """
        tag = Tag(text='test_tag')
        tag.save()

    def tearDown(self):
        """
        Tear down Tag test
        """
        Tag.objects.get(text='test_tag').delete()

    def testGetTag(self):
        """
        Get a single tag
        """
        response = self.client.get('/api/tags/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'text':'test_tag', 'url':'http://testserver/api/tags/1/'})

    def test_get_tag_no_tag(self):
        """
        Get a single tag that doesn't exist
        """
        response = self.client.get('/api/tags/10/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail':'Not found.'})
