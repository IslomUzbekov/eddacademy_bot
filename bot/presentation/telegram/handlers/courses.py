import logging
from urllib.parse import urljoin

from aiogram import F, Router
from aiogram.filters import Command

# Импортируем типы для работы с Telegram API
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from django.conf import settings

# Импортируем функцию для определения языка пользователя
from bot.handlers.common import get_user_language_by_id

# Импортируем функции для генерации клавиатур
from bot.keyboards.inline import get_course_categories_keyboard
from bot.keyboards.reply import get_main_menu_keyboard

# Импортируем сервисы для работы с курсами и текстами
from bot.services.course_service import course_service
from bot.services.text_service import text_service

logger = logging.getLogger(__name__)
router = Router()


# Хэндлер для команды /courses или кнопки "Курсы"
@router.message(Command("courses"))
@router.message(F.text.in_(["Courses", "Курсы", "Kurslar"]))
async def show_course_categories(message: Message):
    """
    Показывает список категорий курсов пользователю.
    """
    lang = await get_user_language_by_id(message.from_user.id)
    categories = await course_service.get_course_categories()

    if not categories:
        # Если категорий нет, отправляем сообщение и главное меню
        await message.answer(
            await text_service.get_text('no_course_categories_found', lang),
            reply_markup=await get_main_menu_keyboard(lang)
        )
        return

    # Отправляем сообщение с просьбой выбрать категорию и клавиатурой
    await message.answer(
        await text_service.get_text('select_course_category', lang),
        reply_markup=await get_course_categories_keyboard(categories, lang)
    )


# Хэндлер для Inline-кнопки "show_course_categories"
# (возврат к категориям из других разделов, например, после просмотра курса)
@router.callback_query(F.data == "show_course_categories")
async def show_course_categories_callback(callback: CallbackQuery):
    """
    Показывает список категорий курсов по callback-запросу.
    """

    if callback.message is None or not isinstance(callback.message, Message):
        await callback.answer("Message is not accessible.", show_alert=True)
        return

    # Используем новую функцию для получения актуального языка
    lang = await get_user_language_by_id(callback.from_user.id)

    categories = await course_service.get_course_categories()

    if not categories:
        # Если категорий нет, редактируем текст сообщения
        # и показываем главное меню
        await callback.message.edit_text(
            await text_service.get_text('no_course_categories_found', lang),
            # reply_markup=None
        )
        await callback.message.answer(
            await text_service.get_text('main_menu_prompt', lang),
            reply_markup=await get_main_menu_keyboard(lang)
        )
        await callback.answer()
        return

    # Показываем категории курсов с клавиатурой
    await callback.message.edit_text(
        await text_service.get_text('select_course_category', lang),
        reply_markup=await get_course_categories_keyboard(categories, lang)
    )
    await callback.answer()


# Хэндлер для показа курсов в выбранной категории (отображает карточки)
@router.callback_query(F.data.startswith("show_courses_in_category_"))
async def show_courses_in_category(callback: CallbackQuery):
    """
    Показывает карточки курсов в выбранной категории с описанием и
    кнопкой "Записаться".
    """
    # Получаем slug категории из callback data
    category_slug = callback.data.split('_')[4]

    if callback.message is None or not isinstance(callback.message, Message):
        await callback.answer("Message is not accessible.", show_alert=True)
        return

    # Используем новую функцию для получения актуального языка
    lang = await get_user_language_by_id(callback.from_user.id)

    category_obj = await course_service.get_course_category_by_slug(
        category_slug
        )

    if not category_obj:
        # Если категория не найдена, показываем ошибку и главное меню
        await callback.answer(
            await text_service.get_text('category_not_found_error', lang),
            show_alert=True
        )
        await callback.message.answer(
            await text_service.get_text('main_menu_prompt', lang),
            reply_markup=await get_main_menu_keyboard(lang)
        )
        return

    # Получаем список курсов в выбранной категории
    courses = await course_service.get_courses_by_category_slug(category_slug)
    # Получаем локализованное название категории
    category_name = getattr(category_obj, f'name_{lang}', category_obj.name_en)

    if not courses:
        # Если курсов нет, редактируем сообщение и
        # показываем клавиатуру с категориями
        await callback.message.edit_text(
            await text_service.get_text(
                'no_courses_in_category_message', lang,
                category_name=category_name
            ),
            reply_markup=await get_course_categories_keyboard(
                await course_service.get_course_categories(), lang)
        )
        await callback.answer()
        return

    # Удаляем сообщение с кнопками категорий,
    # чтобы освободить место для карточек
    await callback.message.delete()

    for course in courses:
        # Получаем локализованные данные курса
        course_title = getattr(course, f'title_{lang}', course.title_en)
        course_description = getattr(
            course, f'description_{lang}', course.description_en
        )

        # Формируем текст карточки курса
        caption_text = await text_service.get_text(
            'course_card_caption',
            lang,
            title=course_title,
            duration=course.duration_months,
            price=f"{course.price:.0f}",
            description=course_description
        )

        # Формируем клавиатуру с кнопкой "Записаться"
        enroll_button_text = await text_service.get_text(
            'enroll_button_text', lang
            )
        enroll_callback_data = f"enroll_course_{course.pk}"
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text=enroll_button_text, callback_data=enroll_callback_data
            )]
        ])

        # Получаем URL изображения курса, если оно есть
        image_url_from_db = getattr(getattr(course, 'image', None), 'url', '')
        full_image_url = ''
        if image_url_from_db.startswith(('http://', 'https://')):
            full_image_url = image_url_from_db
        else:
            full_image_url = urljoin(
                settings.SITE_BASE_URL, image_url_from_db
            )

        # Если есть изображение — отправляем карточку с фото
        # иначе отправляем только текстовую карточку
        if full_image_url:
            await callback.message.answer_photo(
                photo=full_image_url,
                caption=caption_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )
        else:
            await callback.message.answer(
                text=caption_text,
                reply_markup=keyboard,
                parse_mode='HTML'
            )

    # После показа всех курсов отправляем сообщение с кнопкой "Назад"
    back_button_text = await text_service.get_text(
        'back_to_categories_button_text', lang
        )
    back_callback_data = "show_course_categories"
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
    """
    Обрабатывает нажатие на кнопку "Записаться" на курс.
    Сейчас просто показывает заглушку.
    """
    # Получаем id курса из callback data
    course_id = int(callback.data.split('_')[2])

    if callback.message is None or not isinstance(callback.message, Message):
        await callback.answer("Message is not accessible.", show_alert=True)
        return
    # Используем новую функцию для получения актуального языка
    lang = await get_user_language_by_id(callback.from_user.id)

    # Отправляем пользователю плейсхолдер (заглушку) для записи на курс
    await callback.answer(
        await text_service.get_text(
            'enroll_placeholder', lang, course_id=course_id
        ),
        show_alert=True
    )
