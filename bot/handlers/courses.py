import logging

from aiogram import F, Router
from aiogram.filters import Command

# from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

# from django.conf import settings
# Импортируем вспомогательную функцию для получения языка
from bot.handlers.common import (
    get_user_language,
)

# Импортируем клавиатуры
from bot.keyboards.inline import get_course_categories_keyboard
from bot.keyboards.reply import get_main_menu_keyboard

# Импортируем экземпляры сервисов
from bot.services.course_service import course_service
from bot.services.text_service import text_service

logger = logging.getLogger(__name__)
router = Router()


# Хэндлер для команды /courses или кнопки "Курсы"
@router.message(Command("courses"))
@router.message(F.text.in_(["Courses", "Курсы", "Kurslar"]))
async def show_course_categories(
    message: Message,
):
    """
    Показывает список категорий курсов.
    """
    lang = await get_user_language(message)

    categories = await course_service.get_course_categories()

    if not categories:
        await message.answer(
            await text_service.get_text('no_course_categories_found', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        logger.info(f"No course categories found for user {message.from_user.id}. Language: {lang}.")
        return

    await message.answer(
        await text_service.get_text('select_course_category', lang),
        reply_markup=await get_course_categories_keyboard(categories, lang)
    )
    logger.info(f"User {message.from_user.id} requested courses. Displaying categories. Language: {lang}.")


# Хэндлер для Inline-кнопки "show_course_categories"
# (возврат к категориям из других разделов)
@router.callback_query(F.data == "show_course_categories")
async def show_course_categories_callback(
    callback: CallbackQuery,
):
    """
    Показывает список категорий курсов по callback-запросу.
    """
    lang = await get_user_language(callback.message)

    categories = await course_service.get_course_categories()

    if not categories:
        await callback.message.edit_text(
            await text_service.get_text('no_course_categories_found', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        logger.info(f"No course categories found for user {callback.from_user.id} via callback. Language: {lang}.")
        await callback.answer()
        return

    await callback.message.edit_text(
        await text_service.get_text('select_course_category', lang),
        reply_markup=await get_course_categories_keyboard(categories, lang)
    )
    await callback.answer()
    logger.info(f"User {callback.from_user.id} returned to course categories. Language: {lang}.")


# Хэндлер для показа курсов в выбранной категории (теперь отображает карточки)
@router.callback_query(F.data.startswith("show_courses_in_category_"))
async def show_courses_in_category(callback: CallbackQuery):
    """
    Показывает "карточки" курсов в выбранной категории
    с полной информацией и изображением.
    """
    category_slug = callback.data.split('_')[4]
    lang = await get_user_language(callback)
    category_obj = await course_service.get_course_category_by_slug(
        category_slug
        )
    if not category_obj:
        await callback.answer(
            await text_service.get_text('category_not_found_error', lang),
            show_alert=True
        )
        await callback.message.answer(
            await text_service.get_text('main_menu_prompt', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        return

    courses = await course_service.get_courses_by_category_slug(category_slug)

    # Получаем локализованное название категории для заголовка
    # (для сообщения "нет курсов")
    category_name = getattr(category_obj, f'name_{lang}', category_obj.name_en)

    if not courses:
        await callback.message.edit_text(
            await text_service.get_text(
                'no_courses_in_category_message', lang,
                category_name=category_name
                ),
            reply_markup=await get_course_categories_keyboard(
                await course_service.get_course_categories(), lang)
        )
        logger.info(f"No active courses in category '{category_slug}' for user {callback.from_user.id}. Language: {lang}.")
        await callback.answer()
        return

    logger.info(f"User {callback.from_user.id} viewed courses in category '{category_slug}'. Displaying {len(courses)} courses. Language: {lang}.")

    # Удаляем сообщение с кнопками категорий,
    # чтобы освободить место для карточек
    await callback.message.delete()

    for course in courses:
        # Получаем локализованные данные курса
        course_title = getattr(course, f'title_{lang}', course.title_en)
        course_description = getattr(course, f'description_{lang}', course.description_en)

        # Формируем текст "карточки" курса
        # Используем text_service.get_text со слагом 'course_card_caption'
        caption_text = await text_service.get_text(
            'course_card_caption',
            lang,
            title=course_title,
            duration=course.duration_months,
            price=f"{course.price:.0f}",
            description=course_description
        )

        # Формируем кнопки под карточкой
        enroll_button_text = await text_service.get_text(
            'enroll_button_text', lang
            )
        enroll_callback_data = f"enroll_course_{course.id}"

        back_button_text = await text_service.get_text(
            'back_to_categories_button_text', lang
            )
        back_callback_data = "show_course_categories"

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=enroll_button_text, callback_data=enroll_callback_data
                )],
            [InlineKeyboardButton(
                text=back_button_text, callback_data=back_callback_data
                )]
        ])

        if course.image:
            photo_url = course.image.url
            await callback.message.answer_photo(
                photo=photo_url,
                caption=caption_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
        else:
            # Если нет изображения, отправляем просто текст
            await callback.message.answer(
                text=caption_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )

    # После того как все курсы отправлены, можно отправить финальное сообщение
    # чтобы пользователь знал, что ожидается от него дальнейшее действие.
    await callback.answer(
        await text_service.get_text('choose_action_message', lang)
        )
    await callback.message.answer(
        await text_service.get_text('choose_action_message', lang),
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=back_button_text, callback_data=back_callback_data
                )]
        ])
    )


# Хэндлер для кнопки "Записаться" на странице деталей курса (или карточки)
@router.callback_query(F.data.startswith("enroll_course_"))
async def enroll_in_course(callback: CallbackQuery):
    course_id = int(callback.data.split('_')[2])
    lang = await get_user_language(callback.message)

    await callback.answer(
        await text_service.get_text(
            'enroll_placeholder', lang, course_id=course_id
            ),
        show_alert=True
    )
    logger.info(f"User {callback.from_user.id} clicked enroll for course {course_id}. Placeholder shown. Language: {lang}.")
