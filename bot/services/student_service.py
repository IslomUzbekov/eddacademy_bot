# your_telegram_bot_project/bot/services/student_service.py

import logging

from asgiref.sync import sync_to_async
from telegram_bot.models import (
    # Course,
    CourseMaterial,
    ScheduleItem,
    StudentApplication,
    TelegramUser,
)

logger = logging.getLogger(__name__)


class StudentService:
    @sync_to_async
    def get_user_courses(self, telegram_user: TelegramUser):
        """
        Возвращает список курсов, на которые пользователь предположительно
        "зачислен". На данный момент это курсы, на которые пользователь подал
        заявку со статусом 'completed'.
        """

        try:
            # Получаем заявки пользователя со статусом 'completed'
            applications = StudentApplication.objects.filter(
                telegram_user=telegram_user,
                status='completed'
            ).select_related('course').distinct()
            # Извлекаем уникальные курсы из заявок
            enrolled_courses = [
                app.course for app in applications if app.course
                ]

            logger.debug(f"User {telegram_user.user_id} is enrolled in {len(enrolled_courses)} courses.")
            return enrolled_courses
        except Exception as e:
            logger.error(f"Error getting courses for user {telegram_user.user_id}: {e}")
            return []

    @sync_to_async
    def get_course_schedule(self, course_id: int):
        """
        Возвращает расписание для конкретного курса.
        """

        try:
            schedule = list(ScheduleItem.objects.filter(
                course_id=course_id,
                is_active=True,
                lesson_date__gte=timezone.localdate()
            ).order_by('lesson_date', 'lesson_time'))
            logger.debug(f"Retrieved {len(schedule)} schedule items for course {course_id}.")
            return schedule
        except Exception as e:
            logger.error(f"Error getting schedule for course {course_id}: {e}")
            return []

    @sync_to_async
    def get_course_materials(self, course_id: int):
        """
        Возвращает материалы для конкретного курса.
        """

        try:
            materials = list(CourseMaterial.objects.filter(
                course_id=course_id
            ).order_by('title'))
            logger.debug(f"Retrieved {len(materials)} materials for course {course_id}.")
            return materials
        except Exception as e:
            logger.error(f"Error getting materials for course {course_id}: {e}")
            return []


# Создаем единственный экземпляр сервиса
student_service = StudentService()
