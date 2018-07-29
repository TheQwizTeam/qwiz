import json
import logging
from channels import Group, Channel
from channels.sessions import channel_session
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from json.decoder import JSONDecodeError

from quiz.producers import send_response, StatusCode
from .models import Room, Question, Contestant

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

@channel_session
def ws_connect(message):
    # Log endpoint receipt of WebSocket message
    log.debug("WebSocket message received: connect")
    # Accept connection
    message.reply_channel.send({"accept": True})

@channel_session
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
    Channel("quiz.receive").send(payload)

@channel_session
def ws_disconnect(message):
    # Log endpoint receipt of WebSocket message
    log.debug("WebSocket message received: disconnect")

@channel_session
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
    Group(room.group_name()).add(reply_channel)

    # Notify client that request was successfully carried out
    send_response(reply_channel)

    # Published updated contestant list to all contestants
    room.publish_contestant_list()

@channel_session
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
    room.publish_quiz_start()

    # Send a broadcast message to all contestants with the first question
    room.publish_next_question()


@channel_session
def submit_answer(message):
    # Log endpoint receipt of WebSocket message
    log.debug("WebSocket message received: submit_answer")

# @channel_session
# def ws_connect(message):
#     # Extract the room from the message. This expects message.path to be of the
#     # form /quiz/{name}/{handle}/
#     # A Room will be retrieved, and created if it does not already exits.
#     # If the path is invalid, we bail (meaning this is a some othersort
#     # of websocket).
#     try:
#         prefix, room_name, handle = message['path'].decode('ascii').strip('/').split('/')
#         if prefix != 'quiz':
#             log.debug('invalid ws path=%s', message['path'])
#             return
#     except ValueError:
#         log.debug('invalid ws path=%s', message['path'])
#         return
#
#     room, created = Room.objects.get_or_create(name=room_name)
#
#     log.debug('qwiz connect room_name=%s handle=%s client=%s:%s',
#         room.name, handle, message['client'][0], message['client'][1])
#
#     contestant = room.contestant_set.get_or_create(handle=handle)
#
#     # Need to be explicit about the channel layer so that testability works
#     # This may be a FIXME?
#     Group('quiz-'+room.name, channel_layer=message.channel_layer).add(message.reply_channel)
#
#     message.channel_session['room_name'] = room.name
#     message.channel_session['handle'] = contestant.handle
#
# @channel_session
# def ws_receive(message):
#     # Look up the room from the channel session, bailing if it doesn't exist
#     try:
#         room_name = message.channel_session['room_name']
#     except KeyError:
#         log.debug('no room in channel_session')
#         return
#
#     # Parse out a chat message from the content text, bailing if it doesn't
#     # conform to the expected message format.
#     try:
#         data = json.loads(message['text'])
#     except ValueError:
#         log.debug("ws message isn't json text=%s", text)
#         return
#
#     if set(data.keys()) != set(('type', 'handle', 'message')):
#         log.debug("ws message unexpected format data=%s", data)
#         return
#
#     if data:
#         log.debug('chat message room_name=%s type=%s handle=%s message=%s',
#             room_name, data['type'], data['handle'], data['message'])
#
#         type = data['type']
#         contestantHandle = data['handle']
#
#         response_data = {}
#
#         if type == 0:
#             log.debug('NEW ROOM')
#         elif type == 1:
#             log.debug('QUESTION')
#             q = Question.objects.filter(room__name=room_name)[data['message']].questions
#             response_data['type'] = type
#             response_data['question_text'] = q.question_text
#             response_data['correct_answer'] = q.correct_answer
#             response_data['incorrect_answer_1'] = q.incorrect_answer_1
#             response_data['incorrect_answer_2'] = q.incorrect_answer_2
#             response_data['incorrect_answer_3'] = q.incorrect_answer_3
#         elif type == 2:
#             log.debug('RESULT')
#             if (data['message'] == 'correct'):
#                 contestant = Contestant.objects.get(handle=contestantHandle)
#                 contestant.complete=0
#                 contestant.score+=1
#                 contestant.save()
#             response_data['type'] = type
#         elif type == 3:
#             log.debug('SUMMARY')
#             contestants = []
#             finisher = Contestant.objects.get(handle=contestantHandle)
#             finisher.complete = 1;
#             finisher.save()
#             for c in Contestant.objects.filter(room__name=room_name):
#                 contestants.append(tuple((c.handle, c.score)))
#                 if c.complete != 1:
#                     return
#             response_data['type'] = type
#             response_data['scores'] = contestants
#             # Delete all contestants
#             for c in Contestant.objects.filter(room__name=room_name):
#                 c.delete()
#
#         # See above for the note about Group
#         if (type == 0 or type == 1 or type == 2):
#             message.reply_channel.send({'text': json.dumps(response_data)})
#         else :
#             Group('quiz-'+room_name, channel_layer=message.channel_layer).send({'text': json.dumps(response_data)})
