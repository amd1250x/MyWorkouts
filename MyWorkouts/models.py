from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core import validators
import datetime

# Create your models here.


# Workout is a collection of exercises on a given day
class Workout(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    workout_id = models.CharField(validators=[validators.validate_comma_separated_integer_list], max_length=50)
    repsEnd = models.IntegerField()
    repsStart = models.IntegerField()
    setsEnd = models.IntegerField()
    setsStart = models.IntegerField()
    order = models.IntegerField()

    def __str__(self):
        return self.name


class Log(models.Model):
    owner = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)
    exercise_id = models.IntegerField()
    date = models.DateField()
    weight = models.IntegerField()
    reps = models.CharField(max_length=100)

    def __str__(self):
        return self.name
