from __future__ import absolute_import, unicode_literals
from celery import task
import json
from enum import IntEnum, unique
from channels import Channel


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

    if delay:
        channel_send.apply_async(args=(channel, response), countdown=delay)
    else:
        channel_send(channel, response)


@task
def channel_send(channel, response):
    Channel(channel).send({'text': json.dumps(response)})