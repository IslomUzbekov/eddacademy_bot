# your_telegram_bot_project/bot/keyboards/inline.py

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from telegram_bot.models import (
    Course,
    CourseCategory,
    # FAQItem,
)

# from bot.services.student_service import student_service
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
    Каждая кнопка — категория, callback_data содержит slug категории.
    В конце добавляется кнопка "Назад в главное меню".
    """
    keyboard = []
    for category in categories:
        category_name = category.get_localized_name(lang_code)

        keyboard.append([InlineKeyboardButton(
            text=category_name,
            callback_data=f"show_courses_in_category_{category.slug}"
        )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_courses_list_keyboard(
        courses: list[Course],
        lang_code: str) -> InlineKeyboardMarkup:
    """
    Возвращает Inline-клавиатуру со списком курсов
    (например, всех или по категории).
    Каждая кнопка — курс, callback_data содержит id курса.
    """
    keyboard = []
    for course in courses:
        course_name = course.get_localized_title(lang_code)

        keyboard.append([InlineKeyboardButton(
            text=course_name,
            callback_data=f"show_course_details_{course.id}"
        )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_course_details_keyboard(
        course_id: int, lang_code: str) -> InlineKeyboardMarkup:
    """
    Возвращает Inline-клавиатуру с кнопками для деталей курса:
    - "Записаться" (apply_for_course_{course_id})
    - "Назад к списку курсов"
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


async def get_about_us_keyboard(lang_code: str) -> InlineKeyboardMarkup:
    """
    Возвращает локализованную Inline-клавиатуру для раздела 'О нас'.
    Все тексты кнопок берутся из bot_text через text_service.
    """
    history_text = await text_service.get_text(
        'about_us_btn_history', lang_code
        )
    teachers_text = await text_service.get_text(
        'about_us_btn_teachers', lang_code
        )
    partners_text = await text_service.get_text(
        'about_us_btn_partners', lang_code
        )
    achievements_text = await text_service.get_text(
        'about_us_btn_achievements', lang_code
        )
    reviews_text = await text_service.get_text(
        'about_us_btn_reviews', lang_code
        )
    back_text = await text_service.get_text(
        'back_to_main_menu', lang_code
        )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=history_text, callback_data="about_history"
                )],
            [InlineKeyboardButton(
                text=teachers_text, callback_data="about_teachers"
                )],
            [InlineKeyboardButton(
                text=partners_text, callback_data="about_partners"
                )],
            [InlineKeyboardButton(
                text=achievements_text, callback_data="about_achievements"
                )],
            [InlineKeyboardButton(
                text=reviews_text, callback_data="about_reviews"
                )],
            [InlineKeyboardButton(
                text=back_text, callback_data="main_menu"
                )],
        ]
    )
    return keyboard


async def get_back_to_main_menu_keyboard(
        lang_code: str) -> InlineKeyboardMarkup:
    """
    Универсальная клавиатура с одной кнопкой "Назад в главное меню".
    Используется для разделов, где нет подменю
    (например, Новости, Открытые уроки).
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
