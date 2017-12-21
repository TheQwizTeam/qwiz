from django.http import HttpResponse
from django.template import Context, loader
from rest_framework import viewsets
from quiz.models import Tag, Room, Question
from quiz.serialisers import TagSerializer, RoomSerializer, QuestionSerializer


def index(request):
    """
    Render index.html
    """
    template = loader.get_template("index.html")
    return HttpResponse(template.render())


class TagViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows Tags to be viewed
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows Rooms to be viewed
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows Rooms to be viewed
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

