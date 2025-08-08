from xml.dom import ValidationErr

from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from django.db import models

from users.models import User


class Habit(models.Model):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    PERIODICITY_CHOICES = [
        (DAILY, "Ежедневно"),
        (WEEKLY, "Еженедельно"),
        (MONTHLY, "Ежемесячно"),
    ]

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
    periodicity = models.CharField(
        max_length=20,
        choices=PERIODICITY_CHOICES,
        default=DAILY,
        verbose_name="Периодичность",
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

    def clean(self):
        if self.is_pleasant:
            if self.reward:
                raise ValidationError(
                    "У приятной привычки не может быть вознаграждения"
                )
            if self.linked_habit:
                raise ValidationError(
                    "У приятной привычки не может быть связанной привычки"
                )
        else:
            if not self.reward and not self.linked_habit:
                raise ValidationError("У полезной привычки должно быть либо вознаграждение, либо связанная привычка")
            if self.linked_habit and not self.linked_habit.is_pleasant:
                raise ValidationError("Связанная привычка должна быть приятной")

        if self.time_to_complete > 120:
            raise ValidationError("Время выполнения не должно превышать 120 секунд")

class HabitReminder(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='reminders',
        verbose_name='Привычка'
    )
    reminder_time = models.DateTimeField(
        verbose_name='Время напоминания'
    )
    is_sent = models.BooleanField(
        default=False,
        verbose_name='Отправлено'
    )
    chat_id = models.BigIntegerField(
        verbose_name='ID чата в Telegram'
    )

    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания'

    def __str__(self):
        return f"Напоминание для {self.habit} в {self.reminder_time}"


class TelegramUser(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='telegram',
        verbose_name='Пользователь'
    )
    chat_id = models.BigIntegerField(
        unique=True,
        verbose_name='ID чата в Telegram'
    )
    verified = models.BooleanField(
        default=False,
        verbose_name='Подтвержден'
    )
    verification_code = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name='Код подтверждения'
    )

    class Meta:
        verbose_name = 'Telegram пользователь'
        verbose_name_plural = 'Telegram пользователи'

    def __str__(self):
        return f'{self.user} ({self.chat_id})'
