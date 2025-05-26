# your_telegram_bot_project/bot/handlers/common.py

import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    # InlineKeyboardButton,
    # InlineKeyboardMarkup,
    # ReplyKeyboardRemove,
)
from django.conf import settings

# Импортируем клавиатуры
from bot.keyboards.inline import (
    get_back_to_courses_keyboard,
    get_back_to_main_menu_keyboard,
    get_course_categories_keyboard,
    get_course_details_keyboard,
    get_courses_list_keyboard,
    get_faq_list_keyboard,
    get_language_selection_keyboard,
    # get_schedule_materials_back_keyboard,
    # get_student_courses_keyboard,
)
from bot.keyboards.reply import get_main_menu_keyboard

# Импортируем сервисы
from bot.services.course_service import course_service
from bot.services.faq_service import faq_service
from bot.services.news_service import news_service

# from bot.services.open_lesson_service import open_lesson_service
# from bot.services.student_service import student_service
from bot.services.text_service import text_service
from bot.services.user_service import user_service
from bot.states.common_states import LanguageSelection

logger = logging.getLogger(__name__)

router = Router()


# --- Вспомогательная функция для получения языка пользователя ---
async def get_user_language(
        message_or_callback_query: CallbackQuery | Message) -> str:
    """
    Возвращает язык пользователя на основе user_id.
    """
    user_id = message_or_callback_query.from_user.id
    lang = await user_service.get_user_language(user_id)
    return lang


# --- Хэндлер для команды /start ---
@router.message(CommandStart())
async def start_command_handler(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь {message.from_user.id} запустил бота. Username: {
            message.from_user.username}"
        )

    user = await user_service.get_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.language_code
    )
    lang = user.language_code

    await state.clear()

    await message.answer(
        await text_service.get_text(
            'welcome_message', lang, user_name=message.from_user.first_name
            ),
        reply_markup=await get_main_menu_keyboard(lang)
    )
    logger.info(
        f"Пользователь {message.from_user.id} получил приветственное сообщение. Язык: {lang}."
        )

    if lang == settings.DEFAULT_LANGUAGE and message.from_user.language_code and message.from_user.language_code != settings.DEFAULT_LANGUAGE:
        await offer_language_change(message, state, lang)


# --- Хэндлер для кнопки "Главное меню" (callback_data="main_menu") ---
@router.callback_query(F.data == "main_menu")
async def handle_main_menu_button(
    callback_query: CallbackQuery, state: FSMContext):
    logger.info(
        f"User {callback_query.from_user.id} pressed 'Main Menu' button."
        )
    await state.clear()
    lang = await get_user_language(callback_query)

    await callback_query.message.answer(
        await text_service.get_text('main_menu_welcome', lang),
        reply_markup=await get_main_menu_keyboard(lang)
    )
    await callback_query.answer()
    logger.info(
        f"User {callback_query.from_user.id} returned to main menu. Language: {lang}."
        )


# --- Хэндлер для выбора языка ---
@router.callback_query(
        LanguageSelection.waiting_for_language, F.data.startswith("set_lang_")
        )
async def set_language_handler(
    callback_query: CallbackQuery, state: FSMContext):
    new_lang_code = callback_query.data.split('_')[2]
    user_id = callback_query.from_user.id
    logger.info(f"User {user_id} chose language: {new_lang_code}.")

    await user_service.update_user_language(user_id, new_lang_code)
    lang = new_lang_code
    await state.clear()

    await callback_query.message.edit_text(
        await text_service.get_text('language_changed_success', lang),
        reply_markup=None
    )
    await callback_query.message.answer(
        await text_service.get_text('main_menu_welcome', lang),
        reply_markup=await get_main_menu_keyboard(lang)
    )
    await callback_query.answer()
    logger.info(
        f"Language for user {user_id} set to {
            new_lang_code} and main menu displayed."
        )


# --- Хэндлер для кнопки "Новости" ---
@router.message(F.text.in_({'Новости', 'News', 'Yangiliklar'}))
@router.message(F.text.regexp(r'^(Новости|News|Yangiliklar)$'))
async def news_handler(message: Message):
    logger.info(f"User {message.from_user.id} pressed 'News' button.")
    lang = await get_user_language(message)

    news_items = await news_service.get_active_news_items(lang)
    if not news_items:
        await message.answer(await text_service.get_text(
            'no_news_available', lang)
            )
        logger.info(
            f"No active news items found for user {
                message.from_user.id}. Language: {lang}."
            )
        return

    for news_item in news_items:
        caption_text = await text_service.get_text(
            'news_item_caption',
            lang,
            news_title=news_item.get('title', ''),
            news_text=news_item.get('text', ''),
            news_link=news_item.get('link', '')
        )
        if news_item.get('image'):
            await message.answer_photo(
                photo=news_item['image'],
                caption=caption_text,
                reply_markup=await get_back_to_main_menu_keyboard(lang)
            )
        else:
            await message.answer(
                caption_text,
                reply_markup=await get_back_to_main_menu_keyboard(lang)
            )
    logger.info(
        f"User {message.from_user.id} received {
            len(news_items)} news items. Language: {lang}."
        )


# --- Хэндлер для кнопки "Курсы" (Reply-кнопка) и
# callback_data="courses_categories" ---
@router.message(F.text.in_({'Курсы', 'Courses', 'Kurslar'}))
@router.message(F.text.regexp(r'^(Курсы|Courses|Kurslar)$'))
@router.callback_query(F.data == "courses_categories")
async def courses_handler(message_or_callback_query: Message | CallbackQuery):
    logger.info(
        f"User {message_or_callback_query.from_user.id} pressed 'Courses' button or callback."
        )
    lang = await get_user_language(message_or_callback_query)

    categories = await course_service.get_active_course_categories()
    if not categories:
        response_text = await text_service.get_text(
            'no_course_categories_available', lang
            )
        if isinstance(message_or_callback_query, Message):
            await message_or_callback_query.answer(response_text)
        else:
            await message_or_callback_query.message.edit_text(
                response_text, reply_markup=None
                )
            await message_or_callback_query.answer()
        logger.info(
            f"No active course categories found for user {
                message_or_callback_query.from_user.id}."
            )
        return

    response_text = await text_service.get_text('select_course_category', lang)
    reply_markup = await get_course_categories_keyboard(categories, lang)

    if isinstance(message_or_callback_query, Message):
        await message_or_callback_query.answer(
            response_text, reply_markup=reply_markup
            )
    else:
        await message_or_callback_query.message.edit_text(
            response_text, reply_markup=reply_markup
            )
        await message_or_callback_query.answer()
    logger.info(
        f"User {message_or_callback_query.from_user.id} displayed course categories. Language: {lang}."
        )


# --- Хэндлер для Inline-кнопки "Показать курсы по категории" ---
@router.callback_query(F.data.startswith("show_courses_by_category_"))
async def show_courses_by_category_handler(callback_query: CallbackQuery):
    category_slug = callback_query.data.split('_')[4]
    user_id = callback_query.from_user.id
    lang = await get_user_language(callback_query)
    logger.info(
        f"User {user_id} chose category slug: {
            category_slug}. Language: {lang}."
        )

    courses = await course_service.get_courses_by_category_slug(category_slug)
    if not courses:
        await callback_query.message.edit_text(
            await text_service.get_text('no_courses_in_category', lang),
            reply_markup=await get_back_to_courses_keyboard(lang)
        )
        await callback_query.answer()
        logger.info(
            f"No courses found for category '{category_slug}'. User {user_id}."
            )
        return

    response_text = await text_service.get_text(
        'select_course_from_list', lang
        )
    reply_markup = await get_courses_list_keyboard(courses, lang)

    await callback_query.message.edit_text(
        response_text, reply_markup=reply_markup
        )
    await callback_query.answer()
    logger.info(
        f"User {user_id} displayed courses for category '{
            category_slug}'. Found {len(courses)} courses."
        )


# --- Хэндлер для Inline-кнопки "Показать детали курса" ---
@router.callback_query(F.data.startswith("show_course_details_"))
async def show_course_details_handler(callback_query: CallbackQuery):
    course_id = int(callback_query.data.split('_')[3])
    user_id = callback_query.from_user.id
    lang = await get_user_language(callback_query)
    logger.info(
        f"User {user_id} chose course ID: {course_id}. Language: {lang}."
        )

    course = await course_service.get_course_by_id(course_id)
    if not course:
        await callback_query.message.edit_text(
            await text_service.get_text('course_not_found', lang),
            reply_markup=await get_back_to_courses_keyboard(lang)
        )
        await callback_query.answer()
        logger.warning(
            f"Course with ID {course_id} not found for user {user_id}."
            )
        return

    # Получаем локализованные данные курса, используя методы модели Course
    course_title = course.get_localized_title(lang)
    course_description = course.get_localized_description(lang)
    course_benefits = course.get_localized_benefits(lang)
    course_price = course.price

    caption_text = await text_service.get_text(
        'course_details_caption',
        lang,
        course_title=course_title,
        course_description=course_description,
        course_benefits=course_benefits,
        course_price=course_price,
    )

    reply_markup = await get_course_details_keyboard(course.id, lang)

    if course.image:
        await callback_query.message.answer_photo(
            photo=course.image.url,
            caption=caption_text,
            reply_markup=reply_markup
        )
        await callback_query.message.delete()
    else:
        await callback_query.message.edit_text(
            caption_text,
            reply_markup=reply_markup
        )
    await callback_query.answer()
    logger.info(
        f"User {user_id} received details for course ID {
            course_id}. Language: {lang}."
        )


# --- Хэндлер для кнопки "О нас" ---
@router.message(F.text.in_({'О нас', 'About Us', 'Biz haqimizda'}))
@router.message(F.text.regexp(r'^(О нас|About Us|Biz haqimizda)$'))
async def about_us_handler(message: Message):
    logger.info(f"User {message.from_user.id} pressed 'About Us' button.")
    lang = await get_user_language(message)

    about_us_text = await text_service.get_text('about_us_info', lang)
    await message.answer(
        about_us_text,
        reply_markup=await get_back_to_main_menu_keyboard(lang)
    )
    logger.info(
        f"User {
            message.from_user.id} received 'About Us' info. Language: {lang}."
        )


# --- Хэндлер для кнопки "FAQ" ---
@router.message(F.text.in_({'FAQ', 'Вопросы и ответы', 'Savol-Javoblar'}))
@router.message(F.text.regexp(r'^(FAQ|Вопросы и ответы|Savol-Javoblar)$'))
async def faq_handler(message: Message):
    logger.info(f"User {message.from_user.id} pressed 'FAQ' button.")
    lang = await get_user_language(message)

    # Используем faq_service для получения активных FAQ-элементов
    faq_items = await faq_service.get_active_faq_items(lang)
    if not faq_items:
        await message.answer(
            await text_service.get_text('no_faq_available', lang)
            )
        logger.info(
            f"No FAQ items found for user {
                message.from_user.id}. Language: {lang}."
            )
        return

    await message.answer(
        await text_service.get_text('select_faq_question', lang),
        reply_markup=await get_faq_list_keyboard(faq_items, lang)
    )
    logger.info(
        f"User {message.from_user.id} requested FAQ. Displaying {
            len(faq_items)} questions. Language: {lang}."
        )


# --- Хэндлер для Inline-кнопки "Показать ответ на FAQ" ---
@router.callback_query(F.data.startswith("show_faq_answer_"))
async def show_faq_answer_handler(callback_query: CallbackQuery):
    faq_id = int(callback_query.data.split('_')[3])
    user_id = callback_query.from_user.id
    lang = await get_user_language(callback_query)
    logger.info(f"User {user_id} chose FAQ ID: {faq_id}. Language: {lang}.")

    # Используем faq_service для получения конкретного FAQ-элемента
    faq_item = await faq_service.get_faq_item_by_id(faq_id, lang)
    if not faq_item:
        await callback_query.message.edit_text(
            await text_service.get_text('faq_not_found', lang),
            reply_markup=await get_back_to_main_menu_keyboard(lang)
        )
        await callback_query.answer()
        logger.warning(
            f"FAQ item with ID {faq_id} not found for user {user_id}."
            )
        return

    answer_text = await text_service.get_text(
        'faq_answer_caption',
        lang,
        question=faq_item.get('question', ''),
        answer=faq_item.get('answer', '')
    )

    # Возвращаемся к списку FAQ после показа ответа
    await callback_query.message.edit_text(
        answer_text,
        reply_markup=await get_faq_list_keyboard(
            await faq_service.get_active_faq_items(lang), lang
            )
    )
    await callback_query.answer()
    logger.info(
        f"User {user_id} received answer for FAQ ID {
            faq_id}. Language: {lang}."
        )


# Функция для предложения смены языка
async def offer_language_change(
        message: Message,
        state: FSMContext,
        current_lang: str):
    """
    Предлагает пользователю сменить язык, показывая Inline-клавиатуру.
    """

    await message.answer(
        await text_service.get_text('language_selection_prompt', current_lang),
        reply_markup=get_language_selection_keyboard()
    )
    await state.set_state(LanguageSelection.waiting_for_language)
    logger.info(
        f"User {message.from_user.id} requested language change. Setting state to waiting_for_language."
        )


# Хэндлер для всего остального (неизвестные команды/тексты)
@router.message()
async def echo_handler(message: Message):
    """
    Хэндлер для всех остальных сообщений, на которые нет явных правил.
    """

    lang = await get_user_language(message)
    response_text = await text_service.get_text('unknown_command', lang)
    await message.answer(
        response_text,
        reply_markup=await get_main_menu_keyboard(lang)
    )
    logger.info(
        f"User {message.from_user.id} sent unknown message: '{
            message.text}'. Language: {lang}."
        )
