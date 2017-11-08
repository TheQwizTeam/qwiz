"""
Qwiz Models.
"""
from django.db import models
from django.core.exceptions import ValidationError

class Tag(models.Model):
    """
    Tag model used to define question categories.
    Each question can have many tags, and each tag can be associated
    with many questions.
    """
    # Unique value of tag
    text = models.SlugField(unique=True)

    def __str__(self):
        return self.text


class Question(models.Model):
    """
    Question model used to define multiple choice quiz questions.
    Each question has 1 correct answer, 3 incorrect answers and 1 or more tags.
    """
    # Question
    question_text = models.CharField(max_length=200)
    # Correct answer
    correct_answer = models.CharField(max_length=200)
    # Incorrect answers
    incorrect_answer_1 = models.CharField(max_length=200)
    incorrect_answer_2 = models.CharField(max_length=200)
    incorrect_answer_3 = models.CharField(max_length=200)
    # Variable number of tags for a question
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.question_text


class Room(models.Model):
    """
    Room model used to define a quiz room.
    Each room has a name, a unique joining code and a list of questions.
    """
    # Room name, as supplied by user
    name = models.CharField(max_length=200)
    # Unique room code
    code = models.SlugField(unique=True)
    # Variable number of questions in a room
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.name


class Contestant(models.Model):
    """
    Contestant model used to define a quiz contestant.
    Each contestant has a handle (aka name), a score and a completed flag.
    """
    # Room name
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # Handle i.e. username
    handle = models.CharField(max_length=200)
    # Score
    score = models.IntegerField(default=0)
    # has contestant completed
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.handle

    def clean(self):
        if self.room == None:
            raise ValidationError(_('Contestant must be in a Room'))
