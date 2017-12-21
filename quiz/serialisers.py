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
    tags = serializers.ListField(
        write_only=True,
        child=serializers.CharField(write_only=True),
    )
    num_questions = serializers.IntegerField(max_value=10, min_value=1, write_only=True)

    def create(self, validated_data):
        # Remove supplementary data, which will be used to populate the room
        # model with questions once it has been instantiated.
        tags = validated_data.pop('tags')
        num_questions = validated_data.pop('num_questions')

        return super(RoomSerializer, self).create(validated_data)

    class Meta:
        """
        Serialize all fields in the Room object
        """
        model = Room
        fields = ('name', 'code', 'tags', 'num_questions')
        read_only_fields = ('code',)


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
