import re
import json
import logging
from channels import Group
from channels.sessions import channel_session

log = logging.getLogger(__name__)

@channel_session
def ws_connect(message):
    # Extract the room fr:wqom the message. This expects message.path to be of the
    # form /quiz/{room}/{handle}/
    # A Room will be retrieved, and created if it does not already exits.
    # If the path is invalid, we bail (meaning this is a some othersort
    # of websocket). 
    try:
        prefix, room, handle = message['path'].decode('ascii').strip('/').split('/')
        if prefix != 'quiz':
            log.debug('invalid ws path=%s', message['path'])
            return
    except ValueError:
        log.debug('invalid ws path=%s', message['path'])
        return
    log.debug('quiz monster connect room=%s handle=%s client=%s:%s', 
        room, handle, message['client'][0], message['client'][1])
    
    # Need to be explicit about the channel layer so that testability works
    # This may be a FIXME?
    Group('quiz-'+room, channel_layer=message.channel_layer).add(message.reply_channel)

    message.channel_session['room'] = room

@channel_session
def ws_receive(message):
    # Look up the room from the channel session, bailing if it doesn't exist
    try:
        room = message.channel_session['room']
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
    
    if set(data.keys()) != set(('handle', 'message')):
        log.debug("ws message unexpected format data=%s", data)
        return

    if data:
        log.debug('chat message room=%s handle=%s message=%s', 
            room, data['handle'], data['message'])

        # See above for the note about Group
        Group('quiz-'+room, channel_layer=message.channel_layer).send({'text': json.dumps(data)})
