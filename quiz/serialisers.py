from quiz.models import Tag, Room, Question
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
        read_only_fields = ('code', 'questions')
        fields = '__all__'

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """
    Room object serializer
    """
    class Meta:
        """
        Serialize all fields in the Room object
        """
        model = Question
        fields = '__all__'
