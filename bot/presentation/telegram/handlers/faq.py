# # your_telegram_bot_project/bot/handlers/faq.py

# from aiogram import F, Router
# from aiogram.filters import Command
# from aiogram.types import CallbackQuery, Message

# from bot.handlers.common import get_user_language
# from bot.keyboards.inline import get_faq_detail_keyboard, get_faq_list_keyboard
# from bot.keyboards.reply import get_main_menu_keyboard
# from bot.services.faq_service import faq_service
# from bot.services.text_service import text_service
# from bot.services.user_service import UserService

# router = Router()


# # Хэндлер для кнопки "FAQ" или команды /faq
# @router.message(F.text.in_(
#         ["FAQ", "Часто задаваемые вопросы", "Ko'p beriladigan savollar"]
#         ))
# @router.message(Command("faq"))
# # Хэндлер для кнопки "Назад к списку FAQ"
# @router.callback_query(F.data == "show_faq_list")
# async def show_faq(
#     message_or_callback: Message | CallbackQuery,
#     user_service: UserService,
#     text_service: text_service,
#     faq_service: faq_service):
#     """
#     Показывает список активных FAQ-вопросов.
#     """

#     if isinstance(message_or_callback, Message):
#         message = message_or_callback
#         lang = await get_user_language(message)
#     else:
#         callback = message_or_callback
#         message = callback.message
#         lang = await get_user_language(callback.message)

#     faq_items = await faq_service.get_active_faq_items(lang)

#     if not faq_items:
#         await message.answer(
#             await text_service.get_text('no_faq_items', lang)
#             )
#         # Возвращаем в главное меню, если нет FAQ
#         await message.answer(
#             await text_service.get_text('main_menu_prompt', lang),
#             reply_markup=get_main_menu_keyboard(lang)
#             )
#         if isinstance(message_or_callback, CallbackQuery):
#             await callback.answer()
#         return

#     faq_prompt = await text_service.get_text('faq_list_prompt', lang)
#     faq_keyboard = await get_faq_list_keyboard(faq_items, lang)

#     if isinstance(message_or_callback, Message):
#         await message.answer(faq_prompt, reply_markup=faq_keyboard)
#     else:
#         await message.edit_text(faq_prompt, reply_markup=faq_keyboard)
#         await callback.answer()


# @router.callback_query(F.data.startswith('faq_item_'))
# async def show_faq_item_details(
#     callback: CallbackQuery,
#     user_service: UserService,
#     text_service: text_service,
#     faq_service: faq_service):
#     """
#     Показывает ответ на выбранный FAQ-вопрос.
#     """

#     faq_id = int(callback.data.split('_')[2])
#     lang = await get_user_language(callback.message)

#     faq_item = await faq_service.get_faq_item_by_id(faq_id, lang)

#     if faq_item:
#         answer_text = await text_service.get_text(
#             'faq_answer_format',
#             lang,
#             question=faq_item['question'],
#             answer=faq_item['answer']
#             )
#         faq_detail_keyboard = await get_faq_detail_keyboard(lang)
#         await callback.message.edit_text(
#             answer_text,
#             reply_markup=faq_detail_keyboard,
#             parse_mode="Markdown"
#             )
#     else:
#         # Если FAQ не найден (удален, неактивен), возвращаем к списку
#         await callback.message.edit_text(
#             await text_service.get_text('faq_not_found', lang)
#             )
#         await show_faq(callback, user_service, text_service, faq_service)

#     await callback.answer()


# # Хэндлер для возврата в главное меню из любого места,
# # где есть кнопка "back_to_main_menu"
# @router.callback_query(F.data == "back_to_main_menu")
# async def handle_main_menu_button(callback: CallbackQuery):
#     user_id = callback.from_user.id
#     lang = await get_user_language(callback.message)

#     await callback.message.delete()

#     await callback.message.answer(
#         await text_service.get_text('main_menu_prompt', lang),
#         reply_markup=await get_main_menu_keyboard(lang)
#     )
#     await callback.answer()
