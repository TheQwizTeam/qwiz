web: daphne quiz.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
worker: npm start && python manage.py runworker -v2