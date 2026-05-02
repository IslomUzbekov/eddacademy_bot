from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot.handlers.common import get_user_language_by_id
from bot.keyboards.about_us import get_about_us_keyboard
from bot.services.about_us_service import about_us_service

router = Router()

@router.message(Command("about"))
@router.message(F.text.in_(["О нас", "About us"]))
async def about_us_menu(message: Message):
    """
    Показывает меню раздела "О нас".
    """
    lang = await get_user_language_by_id(message.from_user.id)
    await message.answer(
        "<b>О нас</b>\n\nВыберите интересующий раздел:",
        reply_markup=get_about_us_keyboard(lang)
    )

@router.callback_query(F.data.startswith("about_"))
async def about_us_detail(callback: CallbackQuery):
    """
    Показывает подробную информацию по выбранному пункту "О нас".
    """
    lang = await get_user_language_by_id(callback.from_user.id)
    data = callback.data

    if data == "about_history":
        text = await about_us_service.get_history(lang)
    elif data == "about_teachers":
        text = await about_us_service.get_teachers(lang)
    elif data == "about_partners":
        text = await about_us_service.get_partners(lang)
    elif data == "about_achievements":
        text = await about_us_service.get_achievements(lang)
    elif data == "about_reviews":
        text = await about_us_service.get_reviews(lang)
    else:
        await callback.answer("Неизвестный пункт.")
        return

    await callback.message.edit_text(
        text,
        reply_markup=get_about_us_keyboard(lang),
        parse_mode="HTML"
    )
    await callback.answer()
