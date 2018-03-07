import json
from enum import IntEnum, unique
from channels import Channel


@unique
class StatusCode(IntEnum):
    OK = 0
    UNSUPPORTED_COMMAND = 1
    ILLEGAL_ARGUMENT = 2


def send_response(channel, status_code=StatusCode.OK, message=None):
    if not isinstance(status_code, StatusCode):
        raise TypeError('Inappropriate status code')

    response = {
        'status_code': status_code,
    }

    if message:
        response['message'] = message

    Channel(channel).send({'text': json.dumps(response)})
