import logging
from celery import task
from enum import IntEnum, unique

import quiz.models

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@unique
class FutureTask(IntEnum):
    ROOM_PUBLISH_STATUS = 0

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


def schedule(future_task, delay=None, **kwargs):
    future.apply_async(args=(future_task,), kwargs=kwargs, countdown=delay)


@task
def future(future_task, **kwargs):
    if not FutureTask.has_value(future_task):
        raise TypeError("Unknown task {}".format(future_task))

    if future_task == FutureTask.ROOM_PUBLISH_STATUS.value:
        future_publish_status(**kwargs)


def future_publish_status(room_id):
    room = quiz.models.Room.objects.get(pk=room_id)
    room.publish_status()
