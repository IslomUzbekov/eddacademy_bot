# your_telegram_bot_project/bot/keyboards/reply.py

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.services.text_service import text_service


async def get_main_menu_keyboard(lang_code: str) -> ReplyKeyboardMarkup:
    """
    Возвращает Reply-клавиатуру с основным меню бота на выбранном языке.
    """

    news_text = await text_service.get_text('news_button', lang_code)
    courses_text = await text_service.get_text('courses_button', lang_code)
    open_lessons_text = await text_service.get_text(
        'open_lessons_button', lang_code
        )
    apply_course_text = await text_service.get_text(
        'apply_course_button', lang_code
        )
    for_students_text = await text_service.get_text(
        'for_students_button', lang_code
        )
    about_us_text = await text_service.get_text('about_us_button', lang_code)
    faq_text = await text_service.get_text('faq_button', lang_code)
    contact_us_text = await text_service.get_text(
        'contact_us_button', lang_code
        )
    change_language_button = await text_service.get_text(
        "change_language_button", lang_code
        )

    keyboard_buttons = [
        [KeyboardButton(text=news_text),
         KeyboardButton(text=courses_text)],
        [KeyboardButton(text=open_lessons_text),
         KeyboardButton(text=apply_course_text)],
        [KeyboardButton(text=for_students_text),
         KeyboardButton(text=about_us_text)],
        [KeyboardButton(text=faq_text),
         KeyboardButton(text=contact_us_text)],
        [KeyboardButton(text=change_language_button)],
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard_buttons,
        resize_keyboard=True,
        input_field_placeholder=await text_service.get_text(
            'main_menu_placeholder', lang_code
            )
    )
