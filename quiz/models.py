"""
Qwiz Models.
"""
import string
import random
import json

from channels import Group
from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Q


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

    def __init__(self, *args, **kwargs):
        """
        Override the __init__() method to enforce lowercase text.
        """
        super(Tag, self).__init__(*args, **kwargs)
        self.text = self.text.lower()


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

    def populate(self, tags, num_questions):
        """
        Populates this room with a set of questions tagged with any of the passed
        in tags, up to the number of questions requested.
        """
        # A dummy query object (always evaluates to false) that is used as a
        # placeholder for query object bitwise product
        q = Q(pk=None)

        # Bitwise concatenation of tag query objects, filtering questions
        # based on the passed in tags
        for tag in tags:
            q = q | Q(tags__text__exact=tag)

        # Populate room with a random set of questions matching the
        # supplied query, up to the number of questions requested
        questions = list(Question.objects.filter(q).distinct('pk'))
        random.shuffle(questions)
        self.questions.set(questions[:num_questions])

        # Commit questions to the room
        self.save()

        return self

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

    def publish_contestant_list(self):
        """
        Send a 'contestant_list' message from server to client.
        """
        message = {
            "command": "contestant_list",
            "contestants":  [contestant.handle for contestant in self.contestant_set.all()]
        }
        Group('quiz-' + self.code).send({'text': json.dumps(message)})

    def publish_quiz_start(self):
        """
        Send a 'quiz_starting' message from server to client.
        """
        message = {
            "command": "quiz_starting"
        }
        Group('quiz-' + self.code).send({'text': json.dumps(message)})


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
