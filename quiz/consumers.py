import re
import json
import logging
from channels import Group
from channels.sessions import channel_session
from .models import Room, Question, Contestant
#from enum import Enum

log = logging.getLogger(__name__)

#class Color(Enum):
#    NEW_ROOM = 0
#    QUESTION = 1
#    RESULT = 2
#    SUMMARY = 3

@channel_session
def ws_connect(message):
    # Extract the room from the message. This expects message.path to be of the
    # form /quiz/{name}/{handle}/
    # A Room will be retrieved, and created if it does not already exits.
    # If the path is invalid, we bail (meaning this is a some othersort
    # of websocket). 
    try:
        prefix, room_name, handle = message['path'].decode('ascii').strip('/').split('/')
        if prefix != 'quiz':
            log.debug('invalid ws path=%s', message['path'])
            return
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return

    room, created = Room.objects.get_or_create(name=room_name)

    log.debug('quiz monster connect room_name=%s handle=%s client=%s:%s', 
        room.name, handle, message['client'][0], message['client'][1])

    contestant = room.contestant_set.create(handle=handle)
    
    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('quiz-'+room.name, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room_name'] = room.name
    message.channel_session['handle'] = contestant.handle

@channel_session
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        room_name = message.channel_session['room_name']
    except KeyError:
        log.debug('no room in channel_session')
        return

    # Parse out a chat message from the content text, bailing if it doesn't
    # conform to the expected message format.
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", text)
        return
    
    if set(data.keys()) != set(('type', 'handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room_name=%s type=%s handle=%s message=%s', 
            room_name, data['type'], data['handle'], data['message'])

        type = data['type']

        if type == 0:
            log.debug('NEW ROOM')
        elif type == 1:
            log.debug('QUESTION')
        elif type == 2:
            log.debug('RESULT')
        elif type == 3:
            log.debug('SUMMARY')

        # See above for the note about Group
        Group('quiz-'+room_name, channel_layer=message.channel_layer).send({'text': json.dumps(data)})
