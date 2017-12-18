from quiz.models import Tag, Room
from rest_framework import serializers

class TagSerializer(serializers.HyperlinkedModelSerializer):
    """
    Tag object serializer
    """
    class Meta:
        """
        Serialize all fields in the Tag object
        """
        model = Tag
        fields = '__all__'

class RoomSerializer(serializers.HyperlinkedModelSerializer):
    """
    Room object serializer
    """
    class Meta:
        """
        Serialize all fields in the Room object
        """
        model = Room
        fields = '__all__'
