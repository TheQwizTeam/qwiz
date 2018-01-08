from rest_framework import status
from rest_framework.test import APITestCase

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

    def test_get_all_tags(self):
        """
        Get a all tags
        """
        response = self.client.get('/api/tags/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_tag_no_tag(self):
        """
        Get a single tag that doesn't exist
        """
        response = self.client.get('/api/tags/{}/'.format(Tag.objects.last().pk + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {'detail':'Not found.'})

class RestQuestionTests(APITestCase):
    """
    REST API Question test cases.
    """
    def setUp(self):
        """
        Question test setup, creating a single question.
        """
        question = Question(question_text='test_qu')
        question.save()

    def tearDown(self):
        """
        Question test teardown, removing all created Questions
        """
        Question.objects.all().delete()

    def test_get_question(self):
        """
        Get a single question
        """
        last_pk = Question.objects.last().pk
        response = self.client.get('/api/question/{}/'.format(last_pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, \
                {'question_text':'test_qu', 'incorrect_answer_1':'', 'incorrect_answer_2':'', \
                 'incorrect_answer_3':'', 'tags':[], 'correct_answer':'', \
                 'url':'http://testserver/api/question/{}/'.format(last_pk)})

    def test_get_all_questions(self):
        """
        Get a all questions
        """
        response = self.client.get('/api/question/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

class RestRoomTests(APITestCase):
    """
    REST API Room test cases.
    """
    def setUp(self):
        """
        Room test setup, creating a single room
        """
        room = Room(name='test_room')
        room.save()

    def tearDown(self):
        """
        Room test teardown, removing all created rooms
        """
        Room.objects.all().delete()

    def test_get_room(self):
        """
        Get a single room
        """
        last_pk = Room.objects.last().pk
        response = self.client.get('/api/room/{}/'.format(last_pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'name':'test_room', 'code':'{}'.format(Room.objects.last().code)})

    def test_get_all_rooms(self):
        """
        Get a all rooms
        """
        response = self.client.get('/api/room/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
