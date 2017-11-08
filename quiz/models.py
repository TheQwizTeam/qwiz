from django.db import models, transaction, IntegrityError
import string
import random

class Tag(models.Model):
    # Unique value of tag
    text = models.SlugField(unique=True)

    def __str__(self):
        return self.text

class Question(models.Model):
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
    # Room name, as supplied by user
    name = models.CharField(max_length=200)
    # Unique room code
    code = models.SlugField(unique=True, max_length=5)
    # Variable number of questions in a room
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.name

    def code_generator(self, size=5):
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def save(self, *args, **kwargs):
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
    # Contestant's room
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # Handle i.e. username
    handle = models.CharField(max_length=200)
    # user's score
    score = models.IntegerField(default=0)
    # has contestant completed
    complete = models.IntegerField(default=1)

    def __str__(self):
        return self.handle