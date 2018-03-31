from __future__ import absolute_import, unicode_literals

from celery import task
import json
from enum import IntEnum, unique
from channels import Channel, Group

@unique
class StatusCode(IntEnum):
    OK = 0
    UNSUPPORTED_COMMAND = 1
    ILLEGAL_ARGUMENT = 2


def send_response(channel, status_code=StatusCode.OK, message=None, delay=None):
    if not isinstance(status_code, StatusCode):
        raise TypeError('Inappropriate status code')

    response = {
        'status_code': status_code,
    }

    if message:
        response['message'] = message

    send_message(channel, response, delay)


def send_message(target, message, delay=None):
    if target.startswith("quiz-"):
        if delay:
            group_send.apply_async(args=(target, message), countdown=delay)
        else:
            group_send(target, message)
    else:
        if delay:
            channel_send.apply_async(args=(target, message), countdown=delay)
        else:
            channel_send(target, message)


@task
def channel_send(channel, message):
    Channel(channel).send({'text': json.dumps(message)})


@task
def group_send(group, message):
    Group(group).send({'text': json.dumps(message)})
