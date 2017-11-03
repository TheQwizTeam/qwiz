import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Tag, Question, Room, Contestant


class QuizModelTests(TestCase):

    def test_new_room_no_name(self):
        """
        Add a new room with no name.
        """
        r = Room()
        with self.assertRaises(TypeError):
            r.save()

    def test_new_room(self):
        """
        Add a new room.
        """
        r = Room(name='test_room')
        self.assertEqual(r.__str__(), 'test_room')

    def test_new_question_vault_no_str(self):
        """
        Add a new question with no text.
        """
        q = Question()
        with self.assertRaises(TypeError):
            q.save()

    def test_new_question_vault(self):
        """
        Add a new question.
        """
        q = Question(question_text='foo')
        self.assertEqual(q.__str__(), 'foo')

    def test_new_contestant_no_name(self):
        """
        Add a new Contestant with no name.
        """
        c = Contestant()
        with self.assertRaises(TypeError):
            c.save()

    def test_new_contestant(self):
        """
        Add a new Contestant.
        """
        c = Contestant(handle='bob')
        self.assertEqual(c.__str__(), 'bob')
