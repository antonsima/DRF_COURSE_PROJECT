from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    place = models.CharField(max_length=255, verbose_name="Место выполнения")
    time = models.TimeField(verbose_name="Время выполнения")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    linked_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        related_name="linked_habits",
    )
    periodicity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность (в днях)",
    )
    reward = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Вознаграждение"
    )
    time_to_complete = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name="Время на выполнение (в секундах)",
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user}: {self.action} в {self.time} ({self.place})"