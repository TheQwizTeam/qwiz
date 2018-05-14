import re
import logging
from channels import Group, Channel
from channels.sessions import channel_session
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from json.decoder import JSONDecodeError

from quiz.producers import send_response, StatusCode
from .models import Room, Question, Contestant

# New imports
from channels.generic.websocket import AsyncWebsocketConsumer
import json

log = logging.getLogger(__name__)

class QwizConsumer(AsyncWebsocketConsumer):
    """
    New jazz.
    """
    async def connect(self):
        """
        Connection jazz.
        """
        log.debug("WebSocket RX: connect")
        await self.accept()
    
    async def disconnect(self, close_code):
        """
        Disconnection jazz.
        """
        log.debug("WebSocket RX: disconnect")
        pass

    async def receive(self, text_data):
        """
        Websocket receive.
        """
        log.debug("WebSocket RX: receive")
        text_data_json = json.loads(text_data)
        print(text_data_json)
        try:
            payload = json.loads(text_data_json['text'])
        except JSONDecodeError:
            log.error("WS Receive: no data.")
            return HttpResponse(status=400)
        print('Payload: ' + payload)


''' @channel_session
def ws_connect(message):
    # Log endpoint receipt of WebSocket message
    log.debug("WebSocket message received: connect")
    # Accept connection
    message.reply_channel.send({"accept": True}) '''

''' @channel_session
def ws_receive(message):
    # Log endpoint receipt of WebSocket message
    log.debug("WebSocket message received: receive")
    # Route message to "quiz.receive" channel
    try:
        payload = json.loads(message['text'])
    except JSONDecodeError:
        log.error("WS Receive: no data.")
        return HttpResponse(status=400)
    payload['reply_channel'] = message.content['reply_channel']
    Channel("quiz.receive").send(payload) '''

''' @channel_session
def ws_disconnect(message):
    # Log endpoint receipt of WebSocket message
    log.debug("WebSocket message received: disconnect") '''

'''@channel_session
def new_contestant(message):
    # Log endpoint receipt of WebSocket message
    log.debug("WebSocket message received: new_contestant")

    reply_channel = message.get('reply_channel')

    # Attempt to find the room, and create a contestant within this room
    try:
        room = Room.objects.get(code=message.get('room_code'))
        contestant = Contestant(handle=message.get('contestant_name'), room=room)
        contestant.save()
    except ObjectDoesNotExist:
        send_response(reply_channel, StatusCode.ILLEGAL_ARGUMENT, 'The specified room does not exist')
        return

    # Save the room code withing the client's session for convenient future access
    message.channel_session['room_code'] = message.get('room_code')

    # Add the connection's reply channel to the room's connection group
    Group('quiz-' + room.code).add(reply_channel)

    # Notify client that request was successfully carried out
    send_response(reply_channel)

    # Published updated contestant list to all contestants
    room.publish_contestant_list() '''

''' @channel_session
def start_quiz(message):
    # Log endpoint receipt of WebSocket message
    log.debug("WebSocket message received: start_quiz")

    reply_channel = message.get('reply_channel')

    # Attempt to find the room from the session
    try:
        room = Room.objects.get(code=message.channel_session['room_code'])
    except ObjectDoesNotExist:
        send_response(reply_channel, StatusCode.ILLEGAL_ARGUMENT, 'The specified room does not exist')
        return

    # Notify client that request was successfully carried out
    send_response(reply_channel)

    # Send a broadcast message to all contestants to say that the quiz is starting
    room.publish_quiz_start() '''


''' @channel_session
def submit_answer(message):
    # Log endpoint receipt of WebSocket message
    log.debug("WebSocket message received: submit_answer") '''
