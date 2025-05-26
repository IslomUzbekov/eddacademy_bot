# your_telegram_bot_project/bot/keyboards/inline.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telegram_bot.models import (
    Course,
    CourseCategory,
    # FAQItem,
)

from bot.services.student_service import student_service
from bot.services.text_service import text_service


def get_language_selection_keyboard() -> InlineKeyboardMarkup:
    """
    Возвращает Inline-клавиатуру для выбора языка.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🇺🇸 English", callback_data="set_lang_en"
                    ),
                InlineKeyboardButton(
                    text="🇷🇺 Русский", callback_data="set_lang_ru"
                    ),
                InlineKeyboardButton(
                    text="🇺🇿 O'zbek", callback_data="set_lang_uz"
                    )
            ]
        ]
    )
    return keyboard


async def get_course_categories_keyboard(
        categories: list[CourseCategory],
        lang_code: str) -> InlineKeyboardMarkup:
    """
    Возвращает Inline-клавиатуру со списком категорий курсов.
    """
    keyboard = []
    for category in categories:
        category_name = category.get_localized_name(lang_code)

        keyboard.append([InlineKeyboardButton(
            text=category_name,
            callback_data=f"show_courses_by_category_{category.slug}"
        )])

    back_to_main_menu_text = await text_service.get_text(
        'back_to_main_menu', lang_code
        )
    keyboard.append([InlineKeyboardButton(
        text=back_to_main_menu_text, callback_data="main_menu"
        )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_courses_list_keyboard(
        courses: list[Course],
        lang_code: str) -> InlineKeyboardMarkup:
    """
    Возвращает Inline-клавиатуру со списком курсов
    (например, всех или по категории).
    """
    keyboard = []
    for course in courses:
        course_name = course.get_localized_title(lang_code)

        keyboard.append([InlineKeyboardButton(
            text=course_name,
            callback_data=f"show_course_details_{course.id}"
        )])

    # КОММЕНТАРИЙ: Добавляем кнопку "Назад к категориям"
    back_to_categories_text = await text_service.get_text(
        'back_to_categories_button', lang_code
        )
    keyboard.append([InlineKeyboardButton(
        text=back_to_categories_text, callback_data="courses_categories"
        )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_student_courses_keyboard(
        student_id: int, lang_code: str) -> InlineKeyboardMarkup:
    """
    Возвращает Inline-клавиатуру со списком курсов, на которые записан студент.
    """
    keyboard = []
    student_courses_objects = await student_service.get_student_courses(
        student_id
        )

    if student_courses_objects:
        for course_obj in student_courses_objects:
            course_id = course_obj.id
            course_name = course_obj.get_localized_title(lang_code)
            if course_id and course_name:
                keyboard.append([InlineKeyboardButton(
                    text=course_name,
                    callback_data=f"student_course_{course_id}"
                )])

    back_to_main_menu_text = await text_service.get_text(
        'back_to_main_menu', lang_code
        )
    keyboard.append([InlineKeyboardButton(
        text=back_to_main_menu_text, callback_data="main_menu"
        )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_course_details_keyboard(
        course_id: int, lang_code: str) -> InlineKeyboardMarkup:
    """
    Возвращает Inline-клавиатуру с кнопками для деталей курса
    (записаться, назад).
    """
    apply_text = await text_service.get_text('apply_course_button', lang_code)
    back_to_courses_text = await text_service.get_text(
        'back_to_courses_button', lang_code
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=apply_text,
                callback_data=f"apply_for_course_{course_id}"
                )],
            [InlineKeyboardButton(
                text=back_to_courses_text,
                callback_data="courses_categories"
                )],
        ]
    )
    return keyboard


async def get_faq_list_keyboard(
        faq_items: list[dict], lang_code: str) -> InlineKeyboardMarkup:
    """
    Возвращает Inline-клавиатуру со списком вопросов из FAQ.
    """
    keyboard = []
    for item in faq_items:
        question = item['question']
        keyboard.append([InlineKeyboardButton(
            text=question,
            callback_data=f"show_faq_answer_{item['id']}"
        )])

    back_to_main_menu_text = await text_service.get_text(
        'back_to_main_menu', lang_code
        )
    keyboard.append([InlineKeyboardButton(
        text=back_to_main_menu_text, callback_data="main_menu"
        )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_back_to_courses_keyboard(
        lang_code: str) -> InlineKeyboardMarkup:
    """
    Возвращает Inline-клавиатуру с кнопкой "Назад к списку курсов".
    """
    back_to_courses_text = await text_service.get_text(
        'back_to_courses_button', lang_code
        )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=back_to_courses_text,
                callback_data="courses_categories"
                )],
        ]
    )
    return keyboard


async def get_schedule_materials_back_keyboard(
        course_id: int, lang_code: str) -> InlineKeyboardMarkup:
    """
    Возвращает Inline-клавиатуру для возврата из расписания/материалов.
    """
    back_to_student_menu_text = await text_service.get_text(
        'back_to_student_menu_button', lang_code
        )
    back_to_main_menu_text = await text_service.get_text(
        'back_to_main_menu', lang_code
        )

    keyboard = [
        [InlineKeyboardButton(
            text=back_to_student_menu_text,
            callback_data="student_menu"
            )],
        [InlineKeyboardButton(
            text=back_to_main_menu_text,
            callback_data="main_menu"
            )]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_back_to_main_menu_keyboard(
        lang_code: str) -> InlineKeyboardMarkup:
    """
    Универсальная клавиатура с одной кнопкой "Назад в главное меню".
    Используется для разделов, где нет подменю (Новости, Открытые уроки).
    """

    back_to_main_menu_text = await text_service.get_text(
        'back_to_main_menu', lang_code
        )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=back_to_main_menu_text,
                callback_data="main_menu"
            )],
        ]
    )
    return keyboard
