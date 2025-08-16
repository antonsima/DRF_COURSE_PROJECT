from celery import shared_task

from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminder(habit_id: int):
    """Отправка напоминания о привычке."""
    try:
        habit = Habit.objects.get(id=habit_id)
        if not habit.chat_id:
            return

        message = (
            f"⏰ *Напоминание:* {habit.action}\n"
            f"🕒 *Время:* {habit.time.strftime('%H:%M')}\n"
            f"🏠 *Место:* {habit.place}"
        )
        send_telegram_message(habit.chat_id, message)
    except Habit.DoesNotExist:
        print(f"Привычка с ID {habit_id} не найдена.")
