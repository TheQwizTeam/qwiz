"""
Qwiz Models.
"""
import string
import random

from enum import Enum

from django.db import models, transaction, IntegrityError
from django.core.exceptions import ValidationError
from django.db.models import Q

from quiz.future import FutureTask, schedule
from quiz.producers import send_message


class QuestionState(Enum):
    PENDING = "Pending"
    CURRENT = "Current"
    COMPLETE = "Complete"

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

    def shuffled_answers(self):
        answers = [self.correct_answer, self.incorrect_answer_1, self.incorrect_answer_2, self.incorrect_answer_3]
        random.shuffle(answers)
        return answers


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
    questions = models.ManyToManyField(Question, through='RoomQuestions')

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
        [RoomQuestions(room=self, question=question).save() for question in questions[:num_questions]]

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

    def group_name(self):
        """
        Convenience method for generate Room's group name.
        """
        return 'quiz-' + self.code + "-contestant-group"

    def publish_contestant_list(self):
        """
        Send a 'contestant_list' message from server to clients.
        """
        message = {
            "command": "contestant_list",
            "contestants":  [contestant.handle for contestant in self.contestant_set.all()]
        }
        send_message(self.group_name(), message)

    def publish_quiz_start(self):
        """
        Send a 'quiz_starting' message from server to clients.
        """
        message = {
            "command": "quiz_starting"
        }
        send_message(self.group_name(), message)

    def publish_next_question(self, delay=None):
        """
        Get the next question, moving from pending to current
        """
        # Get the next pending question
        question = self.questions.filter(roomquestions__state=QuestionState.PENDING.value).first()
        # Update the question to current
        room_question = self.roomquestions_set.get(question=question.id)
        room_question.state = QuestionState.CURRENT.value
        room_question.save()
        # Publish question
        self.publish_question(question, delay)

    def publish_question(self, question=None, delay=None):
        """
        Send a 'question' message from server to clients.
        """
        # If no question was specified, get the current question
        if question is None:
            question = self.questions.filter(roomquestions__state=QuestionState.CURRENT.value).first()
        # Publish question
        message = {
            "command": "question",
            "question": question.question_text,
            "answers": question.shuffled_answers()
        }
        send_message(self.group_name(), message, delay=delay)
        # Schedule first room summary
        schedule(FutureTask.ROOM_PUBLISH_SUMMARY, room_id=self.id, delay=10+delay)

    def publish_status(self):
        """
        Get the next question, and send 'question' message from server to clients.
        """
        message = {
            "command": "status",
            "answered": [self.status(contestant) for contestant in self.contestant_set.all()]
        }
        send_message(self.group_name(), message)

    def status(self, contestant):
        status = {
            "contestant": contestant.handle,
            "answered": True if contestant.latest_points is not None else False,
        }
        return status


class RoomQuestions(models.Model):
    room = models.ForeignKey(Room, models.DO_NOTHING)
    question = models.ForeignKey(Question, models.DO_NOTHING)
    state = models.CharField(
        max_length=10,
        choices=[(state.name, state.value) for state in QuestionState],
        default=QuestionState.PENDING.value
    )

    class Meta:
        db_table = 'quiz_room_questions'
        unique_together = (('room', 'question'),)


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
    # Has contestant completed
    complete = models.BooleanField(default=False)
    # Score for current question, null if unanswered, 0 if incorrect, positive if correct
    latest_points = models.IntegerField(blank=True, null=True)

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
