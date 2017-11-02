import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Room


class RoomModelTests(TestCase):

    def test_new_room(self):
        """
        Add a new room.
        """
        room = Room(name='test_room')
        self.assertEqual(room.__str__(), 'test_room')
