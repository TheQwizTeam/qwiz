from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=200)

class Question(models.Model):
    # Room
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # Question
    question_text = models.CharField(max_length=200)
    # Answers
    correct_answer = models.CharField(max_length=200)
    incorrect_answer_1 = models.CharField(max_length=200)
    incorrect_answer_2 = models.CharField(max_length=200)
    incorrect_answer_3 = models.CharField(max_length=200)

class Contestant(models.Model):
    handle = models.CharField(max_length=200)
    score = models.IntegerField(default=0)
