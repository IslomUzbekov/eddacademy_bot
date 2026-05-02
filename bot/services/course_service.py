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
        categories = list(
            CourseCategory.objects.filter(is_active=True).order_by('order')
            )
        # logger.info(f"DEBUG: Найдено {len(categories)} активных категорий курса.")
        # for cat in categories:
        #     logger.info(f"DEBUG: Категория: {cat.name_en}, Slug: {cat.slug}, Active: {cat.is_active}")
        return categories

    @sync_to_async
    def get_courses_by_category_slug(self, category_slug: str):
        # logger.info(f"DEBUG: Попытка получить активные курсы для категории slug: '{category_slug}'.")
        try:
            category = CourseCategory.objects.get(
                slug__iexact=category_slug,
                is_active=True
            )
            # logger.info(f"DEBUG: Успешно найдена активная категория по слогу: {category.name_en} (DB Slug: {category.slug}, Received Slug: {category_slug})")

            # if category.slug != category_slug:
            #     logger.warning(f"DEBUG: Несоответствие регистра для slug категории. DB slug: '{category.slug}', Received slug: '{category_slug}'. Продолжаем работу со слизью из БД.")

            courses = list(Course.objects.filter(
                category__slug__iexact=category_slug,
                is_active=True
            ).order_by('title_en'))

            # logger.info(f"DEBUG: Найдено {len(courses)} активных курсов для категории '{category_slug}'.")
            for course in courses:
                if isinstance(course.category, CourseCategory):
                    category_name_for_log = course.category.name_en
                else:
                    if course.category:
                        str(course.category)
                    else:
                        'No Category'

                # logger.info(f"DEBUG: Курс найден: {course.title_en}, Активен: {course.is_active}, Категория: {category_name_for_log}")

            return courses

        except CourseCategory.DoesNotExist:
            # logger.warning(f"DEBUG: Категория со строкой '{category_slug}' не найдена или не активна с помощью iexact.")
            return []

    @sync_to_async
    def get_course_category_by_slug(self, category_slug: str):
        try:
            category = CourseCategory.objects.get(
                slug__iexact=category_slug,
                is_active=True
            )
            # logger.info(f"DEBUG: get_course_category_by_slug: Категория '{category.name_en}' найдена и активна.")
            return category
        except CourseCategory.DoesNotExist:
            # logger.warning(f"DEBUG: get_course_category_by_slug: Категория со словом '{category_slug}' не найдена или не активна.")
            return None


# Создаем единственный экземпляр сервиса
course_service = CourseService()
