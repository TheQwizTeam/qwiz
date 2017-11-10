"""
Qwiz Model unittests.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Tag, Question, Room, Contestant


class TagModelTests(TestCase):
    """
    Tag Model test cases.
    """
    def test_tag(self):
        """
        Add a tag.
        """
        tag = Tag(text='foo_tag')
        tag.save()
        self.assertEqual(str(tag), 'foo_tag')

    def test_tag_no_text(self):
        """
        Add a tag with no text.
        """
        tag1 = Tag()
        with self.assertRaises(ValidationError):
            tag1.full_clean()

    def test_tag_dup(self):
        """
        Add a tag and then a duplicate.
        """
        tag1 = Tag(text='bar_tag')
        tag1.save()
        tag2 = Tag(text='bar_tag')
        with self.assertRaises(ValidationError):
            tag2.full_clean()

    def test_tag_case(self):
        """
        Attempt to add two identical tags with upper/lower case letters.
        """
        tag1 = Tag(text='foo')
        tag1.save()
        tag2 = Tag(text='FOO')
        with self.assertRaises(ValidationError):
            tag2.full_clean()


class QuestionModelTests(TestCase):
    """
    Question Model test cases.
    """
    def test_new_question_no_text(self):
        """
        Add a new question with no text.
        """
        question = Question()
        with self.assertRaises(ValidationError):
            question.full_clean()

    def test_new_question(self):
        """
        Add a new question.
        """
        question = Question(question_text='foo')
        self.assertEqual(str(question), 'foo')


class RoomModelTests(TestCase):
    """
    Room Model test cases.
    """
    def test_room_no_name(self):
        """
        Add a room with no name.
        """
        room = Room()
        with self.assertRaises(ValidationError):
            room.full_clean()

    def test_room(self):
        """
        Add a room.
        """
        room = Room(name='test_room')
        self.assertEqual(str(room), 'test_room')


class ContestantModelTests(TestCase):
    """
    Contestant Model test cases.
    """
    def test_contestant_no_name(self):
        """
        Add a new Contestant with no name.
        """
        room = Room(name='test_room')
        contestant = Contestant(room=room)
        with self.assertRaises(ValidationError):
            contestant.full_clean()

    def test_contestant_no_room(self):
        """
        Add a new Contestant with no room.
        """
        contestant = Contestant(handle='joe')
        with self.assertRaises(Room.DoesNotExist):
            contestant.full_clean()

    def test_contestant(self):
        """
        Add a new Contestant.
        """
        room = Room(name='test_room')
        contestant = Contestant(handle='bob', room=room)
        self.assertEqual(str(contestant), 'bob')
        self.assertEqual(contestant.score, 0)
        self.assertEqual(contestant.complete, False)
