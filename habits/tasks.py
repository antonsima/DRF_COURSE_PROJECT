from celery import shared_task
from django.utils import timezone
from collections import defaultdict

from .models import Habit
from .services import send_telegram_message
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_daily_habit_reminders():
    """
    Отправляет все дневные напоминания о привычках одним сообщением
    Группирует по пользователям
    """
    try:
        today = timezone.now().date()
        weekday = timezone.now().isoweekday()  # 1-7 (пн-вс)

        # Получаем все привычки, которые нужно выполнить сегодня
        habits = Habit.objects.filter(
            periodicity__gte=weekday  # Проверяем периодичность
        ).select_related('user')

        # Группируем привычки по пользователям
        user_habits = defaultdict(list)
        for habit in habits:
            if habit.user.chat_id:
                user_habits[habit.user].append(habit)

        # Формируем и отправляем сообщения
        for user, habits in user_habits.items():
            if not user.chat_id:
                continue

            message = "📅 *Ваши привычки на сегодня:*\n\n"
            for habit in sorted(habits, key=lambda h: h.time):
                message += (
                    f"⏰ *{habit.time.strftime('%H:%M')}* - {habit.action}\n"
                    f"   🏠 {habit.place}\n\n"
                )

            try:
                send_telegram_message(user.chat_id, message)
                logger.info(f"Отправлено дневное напоминание для {user.email}")
            except Exception as e:
                logger.error(f"Ошибка отправки для {user.email}: {str(e)}")

    except Exception as e:
        logger.error(f"Ошибка в задаче send_daily_habit_reminders: {str(e)}")

# @shared_task
# def send_habit_reminders():
#     """
#     Отправляет напоминания о привычках в указанное время
#     с учетом периодичности выполнения
#     """
#     try:
#         now = timezone.now()
#         current_time = now.time()
#         current_weekday = now.isoweekday()  # 1-7 (пн-вс)
#
#         # Находим привычки, которые нужно выполнить сейчас
#         habits = Habit.objects.filter(
#             time__hour=current_time.hour,
#             time__minute=current_time.minute
#         )
#
#         for habit in habits:
#             # Проверяем периодичность (если 1 - ежедневно, 7 - раз в неделю)
#             if habit.periodicity == 1 or habit.periodicity >= current_weekday:
#                 if not habit.user.chat_id:
#                     logger.warning(f"У пользователя {habit.user} не указан chat_id")
#                     continue
#
#                 message = (
#                     f"⏰ *Напоминание:* {habit.action}\n"
#                     f"🕒 *Время:* {habit.time.strftime('%H:%M')}\n"
#                     f"🏠 *Место:* {habit.place}"
#                 )
#
#                 try:
#                     send_telegram_message(habit.user.chat_id, message)
#                     logger.info(f"Отправлено напоминание для {habit.user}: {habit.action}")
#                 except Exception as e:
#                     logger.error(f"Ошибка отправки сообщения: {str(e)}")
#
#     except Exception as e:
#         logger.error(f"Ошибка в задаче send_habit_reminders: {str(e)}")