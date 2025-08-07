import datetime

from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField()
    time = models.DateTimeField()
    action = models.CharField()
    is_good_habit = models.BooleanField()
    linked_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL)
    period = models.DateTimeField(default=datetime.datetime(day=1))
    reward = models.CharField()
    time_to_complete = models.TimeField()
    is_public = models.BooleanField()

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

