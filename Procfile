web: daphne quiz.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
channelsworker: python manage.py runworker -v2
celeryworker: celery worker -A quiz --loglevel debug
