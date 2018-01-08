from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Tag, Question, Room, Contestant


class RestTagTests(APITestCase):
    """
    REST API Tag test cases.
    """
    def setUp(self):
        """
        Tag test setup, creating a single tag.
        """
        tag = Tag(text='test_tag')
        tag.save()

    def tearDown(self):
        """
        Tag test teardown, removing all created Tags
        """
        Tag.objects.all().delete()

    def test_get_tag(self):
        """
        Get a single tag
        """
        last_pk = Tag.objects.last().pk
        response = self.client.get('/api/tags/{}/'.format(last_pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'text':'test_tag', 'url':'http://testserver/api/tags/{}/'.format(last_pk)})

    def test_get_tag_no_tag(self):
        """
        Get a single tag that doesn't exist
        """
        response = self.client.get('/api/tags/{}/'.format(Tag.objects.last().pk + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail':'Not found.'})
