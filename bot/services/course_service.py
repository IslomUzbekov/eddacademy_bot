# bot/services/course_service.py

import logging

from asgiref.sync import sync_to_async
from telegram_bot.models import Course, CourseCategory

logger = logging.getLogger(__name__)


class CourseService:
    """
    Сервис для работы с курсами учебного центра.
    Отвечает за получение информации о курсах.
    """

    @sync_to_async
    def get_active_courses(self):
        """
        Возвращает список всех активных курсов.
        """
        return list(Course.objects.filter(is_active=True).order_by('title_en'))

    # @sync_to_async
    # def get_course_by_localized_title(self, title: str, lang_code: str):
    #     """
    #     Возвращает курс по его названию.
    #     """
    #     try:
    #         return Course.objects.get(title_en__iexact=title, is_active=True)
    #     except Course.DoesNotExist:
    #         return None

    @sync_to_async
    def get_course_by_id(self, course_id: int):
        """
        Возвращает курс по его ID.
        """
        try:
            return Course.objects.get(id=course_id, is_active=True)
        except Course.DoesNotExist:
            return None

    @sync_to_async
    def get_course_categories(self):
        categories = list(CourseCategory.objects.filter(is_active=True).order_by('order'))
        logger.info(f"DEBUG: Found {len(categories)} active course categories.")
        for cat in categories:
            logger.info(f"DEBUG: Category: {cat.name_en}, Slug: {cat.slug}, Active: {cat.is_active}")
        return categories

    @sync_to_async
    def get_courses_by_category_slug(self, category_slug: str):
        logger.info(f"DEBUG: Attempting to fetch active courses for category slug: '{category_slug}'.")
        try:
            category = CourseCategory.objects.get(
                slug__iexact=category_slug,
                is_active=True
            )
            logger.info(f"DEBUG: Successfully found active category by slug: {category.name_en} (DB Slug: {category.slug}, Received Slug: {category_slug})")

            if category.slug != category_slug:
                logger.warning(f"DEBUG: Case mismatch for category slug. DB slug: '{category.slug}', Received slug: '{category_slug}'. Proceeding with DB slug.")

            courses = list(Course.objects.filter(
                # category=category.id,
                category__slug__iexact=category_slug,
                is_active=True
            ).order_by('title_en'))

            logger.info(f"DEBUG: Found {len(courses)} active courses for category '{category_slug}'.")
            for course in courses:
                category_name_for_log = course.category.name_en if isinstance(course.category, CourseCategory) else (str(course.category) if course.category else 'No Category')
                logger.info(f"DEBUG: Course found: {course.title_en}, Is active: {course.is_active}, Category: {category_name_for_log}")

            return courses

        except CourseCategory.DoesNotExist:
            logger.warning(f"DEBUG: Category with slug '{category_slug}' not found or not active using iexact.")
            return []

    @sync_to_async
    def get_course_category_by_slug(self, category_slug: str):
        try:
            category = CourseCategory.objects.get(
                slug__iexact=category_slug,
                is_active=True
            )
            logger.info(f"DEBUG: get_course_category_by_slug: Category '{category.name_en}' found and active.")
            return category
        except CourseCategory.DoesNotExist:
            logger.warning(f"DEBUG: get_course_category_by_slug: Category with slug '{category_slug}' not found or not active.")
            return None


# Создаем единственный экземпляр сервиса
course_service = CourseService()
