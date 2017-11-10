"""
Qwiz Models.
"""
import string
import random
from django.db import models, transaction, IntegrityError
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
        """
        Stringify a Tag.
        """
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
        """
        Stringify a Question.
        """
        return self.question_text


class Room(models.Model):
    """
    Room model used to define a quiz room.
    Each room has a name, a unique joining code and a list of questions.
    """
    # Room name, as supplied by user
    name = models.CharField(max_length=200)
    # Unique room code
    code = models.SlugField(unique=True, max_length=5)
    # Variable number of questions in a room
    questions = models.ManyToManyField(Question)

    def __str__(self):
        """
        Stringify a Room.
        """
        return self.name

    def code_generator(self, size=5):
        """
        Generate a random Room code containg 'size' lowercase characters
        and digits.
        """
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
        """
        Room save method. Override the default method to generate a room code
        and ensure it's unique.
        """
        # Generate a unique code for the room
        if not self.code:
            self.code = self.code_generator()
        # Save the room. If the code clashes generate a new one and try again.
        while True:
            try:
                with transaction.atomic():
                    return super(Room, self).save(*args, **kwargs)
            except IntegrityError:
                self.code = self.code_generator()


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
        """
        Stringify the contestant.
        """
        return self.handle

    def clean(self):
        """
        Model validation.
        """
        if self.room is None:
            raise ValidationError(_('Contestant must be in a Room'))
