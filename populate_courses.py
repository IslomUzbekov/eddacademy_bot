import os

import django


def main():
    # 1. Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE.
    # Эта строка ДОЛЖНА БЫТЬ ПЕРВОЙ ЛОГИЧЕСКОЙ ОПЕРАЦИЕЙ В СКРИПТЕ.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings') # ИСПОЛЬЗУЕМ 'core.settings'

    # 2. Инициализируем Django окружение.
    # Этот вызов ДОЛЖЕН СТОЯТЬ СРАЗУ ПОСЛЕ УСТАНОВКИ DJANGO_SETTINGS_MODULE.
    django.setup()

    # 3. ТЕПЕРЬ, когда Django полностью инициализирован и его настройки доступны,
    # можно безопасно импортировать Django-модели и другие части Django.
    # Обратите внимание: импорты моделей находятся ВНУТРИ функции main(),
    # чтобы они не выполнялись до django.setup().
    from django.db import transaction
    from telegram_bot.models import Course, CourseCategory

    print("--- Starting course and category recreation script ---")

    try:
        with transaction.atomic():
            # 1. Удаляем все существующие курсы
            Course.objects.all().delete()
            print("All existing courses deleted.")

            # 2. Удаляем все существующие категории курсов
            CourseCategory.objects.all().delete()
            print("All existing course categories deleted.")

            # 3. Создаем категории заново
            print("\nCreating new course categories...")
            cat_programming = CourseCategory.objects.create(
                name_ru='Программирование',
                name_en='Programming',
                name_uz='Dasturlash',
                slug='programming',
                order=10,
                is_active=True
            )
            print(f"Created category: {cat_programming.name_en} (ID: {cat_programming.id})")

            cat_design = CourseCategory.objects.create(
                name_ru='Дизайн',
                name_en='Design',
                name_uz='Dizayn',
                slug='design',
                order=20,
                is_active=True
            )
            print(f"Created category: {cat_design.name_en} (ID: {cat_design.id})")

            cat_robotics = CourseCategory.objects.create(
                name_ru='Робототехника',
                name_en='Robotics',
                name_uz='Robototexnika',
                slug='robotics',
                order=30,
                is_active=True
            )
            print(f"Created category: {cat_robotics.name_en} (ID: {cat_robotics.id})")

            cat_architecture = CourseCategory.objects.create(
                name_ru='Архитектура',
                name_en='Architecture',
                name_uz='Arxitektura',
                slug='architecture',
                order=40,
                is_active=True
            )
            print(f"Created category: {cat_architecture.name_en} (ID: {cat_architecture.id})")

            cat_languages = CourseCategory.objects.create(
                name_ru='Языки',
                name_en='Languages',
                name_uz='Tillar',
                slug='languages',
                order=50,
                is_active=True
            )
            print(f"Created category: {cat_languages.name_en} (ID: {cat_languages.id})")

            cat_others = CourseCategory.objects.create(
                name_ru='Прочее',
                name_en='Others',
                name_uz='Boshqalar',
                slug='others',
                order=60,
                is_active=True
            )
            print(f"Created category: {cat_others.name_en} (ID: {cat_others.id})")

            # 4. Создаем курсы заново и связываем их с категориями
            print("\nCreating new courses...")
            course_backend = Course.objects.create(
                title_ru='Backend Разработка',
                title_en='Backend Development',
                title_uz='Backend Ishlab chiqish',
                description_ru='Подробное описание курса Backend Development.',
                description_en='Detailed description of Backend Development course.',
                description_uz='Backend ishlab chiqish kursining batafsil tavsifi.',
                duration_months=6,
                price=500000,
                category=cat_programming,  # Привязываем к объекту категории
                is_active=True
            )
            print(f"Created course: {course_backend.title_en} (ID: {course_backend.id}) in {cat_programming.name_en} category.")

            course_frontend = Course.objects.create(
                title_ru='Frontend Разработка',
                title_en='Frontend Development',
                title_uz='Frontend Ishlab chiqish',
                description_ru='Подробное описание курса Frontend Development.',
                description_en='Detailed description of Frontend Development course.',
                description_uz='Frontend ishlab chiqish kursining batafsil tavsifi.',
                duration_months=5,
                price=450000,
                category=cat_programming,  # Привязываем к объекту категории
                is_active=True
            )
            print(f"Created course: {course_frontend.title_en} (ID: {course_frontend.id}) in {cat_programming.name_en} category.")

            course_english = Course.objects.create(
                title_ru='Английский для IT',
                title_en='English for IT',
                title_uz='IT uchun Ingliz tili',
                description_ru='Изучение английского языка для IT-специалистов.',
                description_en='Learning English for IT professionals.',
                description_uz='IT mutaxassislari uchun ingliz tilini o\'rganish.',
                duration_months=4,
                price=300000,
                category=cat_languages,
                is_active=True
            )
            print(f"Created course: {course_english.title_en} (ID: {course_english.id}) in {cat_languages.name_en} category.")

            print("\n--- Courses and categories recreation script finished successfully! ---")

    except Exception as e:
        print(f"\n--- An error occurred: {e} ---")
        import traceback
        traceback.print_exc()  # Для более подробного вывода ошибки


if __name__ == "__main__":
    main()  # Вызываем обернутую функцию
