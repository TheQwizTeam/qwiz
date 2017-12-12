from django.http import HttpResponse
from django.template import Context, loader
from rest_framework import viewsets
from quiz.models import Tag
from quiz.serialisers import TagSerializer

def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

class TagViewSet(viewsets.ModelViewSet):
    """
    API Endpoint that allows tags to be viewed
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    