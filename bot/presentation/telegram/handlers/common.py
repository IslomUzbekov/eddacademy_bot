import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
    # InlineKeyboardMarkup,
    # ReplyKeyboardMarkup,
)
from django.conf import settings
from telegram_bot.models import TelegramUser

# Импортируем клавиатуры
from bot.keyboards.inline import (
    # get_back_to_courses_keyboard,
    # get_back_to_main_menu_keyboard,
    # get_course_categories_keyboard,
    # get_course_details_keyboard,
    # get_courses_list_keyboard,
    # get_faq_list_keyboard,
    get_language_selection_keyboard,
    # get_schedule_materials_back_keyboard,
    # get_student_courses_keyboard,
)
from bot.keyboards.reply import get_main_menu_keyboard

# from bot.services.course_service import course_service
# from bot.services.faq_service import faq_service
# from bot.services.news_service import news_service
# Импортируем сервисы
# from bot.services.open_lesson_service import open_lesson_service
# from bot.services.student_service import student_service
from bot.services.text_service import text_service
from bot.services.user_service import user_service
from bot.states.common_states import LanguageSelection

logger = logging.getLogger(__name__)

router = Router()


# --- Хэндлер для получения языка ползователья из БД ---
async def get_user_language_by_id(user_id: int) -> str:
    """
    Определяет язык пользователя по его user_id.
    1. Если пользователь есть в базе — возвращает его язык.
    2. Если нет — возвращает 'ru' (или ваш DEFAULT_LANGUAGE).
    """
    user = await user_service.get_user_by_id(user_id)
    if user and user.language_code:
        return user.language_code
    return settings.DEFAULT_LANGUAGE


# --- Хэндлер для команды /start ---
@router.message(CommandStart())
async def start_command_handler(message: Message, state: FSMContext):

    user_object, created = await user_service.get_or_create_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        language_code=message.from_user.language_code,
        is_bot=message.from_user.is_bot
    )

    lang = user_object.language_code

    if created:
        await message.answer(
            await text_service.get_text('welcome_new_user', lang),
            reply_markup=await get_main_menu_keyboard(lang)
        )
        await offer_language_change(message, state, lang)
    else:
        await message.answer(
            await text_service.get_text('welcome_back_user', lang),
            reply_markup=await get_main_menu_keyboard(lang)
        )

    await state.clear()


# --- Хэндлер для кнопки "Сменить язык" ---
@router.message(
        F.text.in_({
            'Сменить язык',
            'Tilni o\'zgartirish',
            'Change language'
        }) |
        (F.text == 'Change Language') |
        (F.text.func(lambda text: text.strip() == 'Change Language'))
    )
async def change_language_handler(message: Message, state: FSMContext):
    current_lang = await get_user_language_by_id(message.from_user.id)
    await offer_language_change(message, state, current_lang)


# --- Хэндлер для выбора языка из инлайн-клавиатуры ---
@router.callback_query(
    LanguageSelection.waiting_for_language, F.data.startswith('set_lang_')
)
async def set_language_callback_handler(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    selected_lang = callback_query.data.split('_')[2]
    success = await user_service.set_user_language(user_id, selected_lang)
    confirmation_text = await text_service.get_text(
        'language_changed_confirmation', selected_lang
        )

    if success:

        await callback_query.answer(
            text=confirmation_text, show_alert=False
            )
        await callback_query.message.edit_text(
            confirmation_text
            )

        await callback_query.message.answer(
            await text_service.get_text('main_menu_prompt', selected_lang),
            reply_markup=await get_main_menu_keyboard(selected_lang)
        )
        await state.clear()
    else:
        await callback_query.message.answer(
            await text_service.get_text('language_change_error', selected_lang)
        )


# --- Функция для предложения смены языка ---
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


# --- Хэндлер для всего остального (неизвестные команды/тексты) ---
@router.message()
async def echo_handler(message: Message):
    """
    Хэндлер для всех остальных сообщений, на которые нет явных правил.
    """

    lang = await get_user_language_by_id(message.from_user.id)
    response_text = await text_service.get_text('unknown_command', lang)
    await message.answer(
        response_text,
        reply_markup=await get_main_menu_keyboard(lang)
    )
