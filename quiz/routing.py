''' from channels.staticfiles import StaticFilesConsumer
from .consumers import ws_connect, ws_receive, ws_disconnect, new_contestant, start_quiz, submit_answer
from channels import include, route '''

from django.conf.urls import url
from . import consumers

websocket_urlpatterns = [
    url(r'^ws/(?P<room_name>[^/]+)/$', consumers.QwizConsumer),
]

''' # Although we could, there is no path matching on these routes; instead we rely
# on the matching from the top-level routing.
websocket_routing = [
    # This makes Django serve static files from settings.STATIC_URL, similar
    # to django.views.static.serve. This isn't ideal (not exactly production
    # quality) but it works for a minimal example.
    route('http.request', StaticFilesConsumer()),

    # Called when WebSockets connect
    route("websocket.connect", ws_connect),

    # Called when WebSockets get sent a data frame
    route("websocket.receive", ws_receive),

    # Called when WebSockets disconnect
    route("websocket.disconnect", ws_disconnect),
]

channel_routing = [
    # Handling different quiz commands (websocket.receive is decoded and put
    # onto this channel) - routed on the "command" attribute of the decoded
    # message.
    route("quiz.receive", new_contestant, command="^new_contestant$"),
    route("quiz.receive", start_quiz, command="^start_quiz$"),
    route("quiz.receive", submit_answer, command="^submit_answer$"),
    include("quiz.routing.websocket_routing"),
] '''