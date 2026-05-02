# # your_telegram_bot_project/bot/services/open_lesson_service.py

# import logging

# from asgiref.sync import sync_to_async
# from django.utils import timezone
# from telegram_bot.models import OpenLesson

# logger = logging.getLogger(__name__)


# class OpenLessonService:
#     @sync_to_async
#     def get_upcoming_open_lessons(self):
#         """
#         Возвращает активные открытые уроки, запланированные на будущее
#         (включая сегодня), отсортированные по дате и времени.
#         """
#         today = timezone.localdate()
#         try:
#             lessons = list(OpenLesson.objects.filter(
#                 is_active=True,
#                 lesson_date__gte=today
#             ).order_by('lesson_date', 'lesson_time'))
#             logger.debug(f"Извлечение {len(lessons)} предстоящих открытых уроков.")
#             return lessons
#         except Exception as e:
#             logger.error(f"Ошибка при получении предстоящих открытых уроков: {e}")
#             return []


# # Создаем единственный экземпляр сервиса
# open_lesson_service = OpenLessonService()
