from channels.test import ChannelTestCase, Client, WSClient

from quiz.producers import StatusCode
from .models import Tag, Question, Room, Contestant


class WebSocketCreateContestantTests(ChannelTestCase):
    """
    WebSocket create contestant through WebSocket API tests
    """
    def setUp(self):
        """
        Room test setup, creating a single room
        """
        room = Room(name='Test Room')
        room.save()

    def tearDown(self):
        """
        Room test teardown, removing all created rooms
        """
        Room.objects.all().delete()

    def test_create_contestant_invalid_room(self):
        """
        Attempt to create a contestant in an invalid room
        """
        client = WSClient()
        client.send_and_consume('websocket.connect')
        client.send_and_consume('quiz.receive',{
            'command': 'new_contestant',
            'room_code': '12345',
            'contestant_name': 'Joe Bloggs'
        })

        response = client.receive()

        # Verify server responded with correct status code
        self.assertEqual(response['status_code'], StatusCode.ILLEGAL_ARGUMENT)
        # Verify contestant count remains zero
        self.assertEquals(Contestant.objects.all().count(), 0)

        client.send_and_consume('websocket.disconnect')

    def test_create_contestant_ialid_room(self):
        """
        Attempt to create a contestant in a valid room
        """
        room = Room.objects.last()

        client = WSClient()
        client.send_and_consume('websocket.connect')
        client.send_and_consume('quiz.receive',{
            'command': 'new_contestant',
            'room_code': room.code,
            'contestant_name': 'Joe Bloggs'
        })

        response = client.receive()

        # Verify server responded with correct status code
        self.assertEqual(response['status_code'], StatusCode.OK)
        # Verify room contestant count is one
        self.assertEquals(room.contestant_set.count(), 1)
        # Verify it is indeed Joe Bloggs in the room
        self.assertEquals(room.contestant_set.last().handle, 'Joe Bloggs')

        client.send_and_consume('websocket.disconnect')