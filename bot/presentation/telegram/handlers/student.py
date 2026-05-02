# # your_telegram_bot_project/bot/handlers/student.py

# import logging

# from aiogram import F, Router
# from aiogram.fsm.context import FSMContext
# from aiogram.types import CallbackQuery, Message

# from bot.keyboards.inline import (
#     get_schedule_materials_back_keyboard,
#     get_student_menu_keyboard,
# )
# from bot.services.student_service import student_service
# from bot.services.text_service import text_service
# from bot.services.user_service import user_service

# # from bot.states.student_states import StudentNavigation

# logger = logging.getLogger(__name__)

# router = Router()


# # Вспомогательная функция (можно импортировать из common)
# async def get_user_language(
#         message_or_callback: Message | CallbackQuery) -> str:
#     user_id = message_or_callback.from_user.id
#     telegram_user = await user_service.get_user_by_id(user_id)
#     return telegram_user.language_code if telegram_user and telegram_user.language_code else 'en'


# @router.callback_query(F.data.startswith("student_course_"))
# async def show_student_course_menu(callback: CallbackQuery, state: FSMContext):
#     """
#     Показывает меню для выбранного курса студента (Расписание, Материалы).
#     """

#     course_id = int(callback.data.split('_')[2])
#     lang = await get_user_language(callback)

#     # Сохраняем ID выбранного курса в состояние для дальнейшей навигации
#     await state.update_data(current_student_course_id=course_id)
#     # await state.set_state(StudentNavigation.viewing_course_menu)

#     await callback.message.edit_text(
#         await text_service.get_text('student_course_menu_prompt', lang),
#         reply_markup=await get_student_menu_keyboard(lang)
#     )
#     await callback.answer()
#     logger.info(f"Пользователь {callback.from_user.id} выбрал курс {course_id}. Отображение меню курса. Язык: {lang}.")


# @router.callback_query(F.data == "show_student_schedule")
# async def show_student_schedule(callback: CallbackQuery, state: FSMContext):
#     """
#     Показывает расписание для выбранного курса студента.
#     """
#     lang = await get_user_language(callback)
#     data = await state.get_data()
#     course_id = data.get('current_student_course_id')

#     if not course_id:
#         await callback.message.edit_text(
#             await text_service.get_text('error_no_course_selected', lang) +
#             "\n" + await text_service.get_text('main_menu_prompt', lang),
#             reply_markup=await get_main_menu_keyboard(lang)
#         )
#         await callback.answer(await text_service.get_text('error_no_course_selected', lang), show_alert=True)
#         return

#     schedule_items = await student_service.get_course_schedule(course_id)

#     if not schedule_items:
#         response_text = await text_service.get_text(
#             'no_schedule_available', lang)
#     else:
#         response_text = await text_service.get_text('schedule_prompt', lang)
#         for item in schedule_items:
#             response_text += (
#                 f"\n\n*_{item.lesson_date.strftime('%d.%m.%Y')} {item.lesson_time}_*\n"
#                 f"*{item.title}*\n"
#                 f"{item.description or ''}"
#             )

#     await callback.message.edit_text(
#         response_text,
#         reply_markup=await get_schedule_materials_back_keyboard(
#             course_id, lang),
#         parse_mode="Markdown"
#     )
#     await callback.answer()
#     logger.info(f"Пользователь {callback.from_user.id} просмотрел расписание для курса {course_id}. Язык: {lang}.")


# @router.callback_query(F.data == "show_student_materials")
# async def show_student_materials(callback: CallbackQuery, state: FSMContext):
#     """
#     Показывает материалы для выбранного курса студента.
#     """

#     lang = await get_user_language(callback)
#     data = await state.get_data()
#     course_id = data.get('current_student_course_id')

#     if not course_id:
#         await callback.message.edit_text(
#             await text_service.get_text('error_no_course_selected', lang) +
#             "\n" + await text_service.get_text('main_menu_prompt', lang),
#             reply_markup=await get_main_menu_keyboard(lang)
#         )
#         await callback.answer(await text_service.get_text(
#             'error_no_course_selected', lang), show_alert=True)
#         return

#     materials = await student_service.get_course_materials(course_id)

#     if not materials:
#         response_text = await text_service.get_text(
#             'no_materials_available', lang)
#     else:
#         response_text = await text_service.get_text('materials_prompt', lang)
#         for material in materials:
#             link_text = ""
#             if material.url:
#                 link_text = f" [Ссылка]({material.url})"
#             elif material.file:
#                 link_text = " [Файл прикреплен]"

#             response_text += (
#                 f"\n\n*{material.title}*\n"
#                 f"{material.description or ''}{link_text}"
#             )

#     await callback.message.edit_text(
#         response_text,
#         reply_markup=await get_schedule_materials_back_keyboard(
#             course_id, lang),
#         parse_mode="Markdown"
#     )
#     await callback.answer()
#     logger.info(f"Пользователь {callback.from_user.id} просмотрел материалы для курса {course_id}. Язык: {lang}.")

# @router.callback_query(F.data == "show_student_courses_list")
# async def return_to_student_courses_list(
#     callback: CallbackQuery, state: FSMContext):
#     """
#     Возвращает пользователя к списку его курсов из студенческого меню.
#     """

#     lang = await get_user_language(callback)
#     user_telegram_obj = await user_service.get_user_by_id(
#         callback.from_user.id)
#     student_courses = await student_service.get_user_courses(user_telegram_obj)

#     if not student_courses:
#         response_text = await text_service.get_text('no_student_courses', lang)
#         await callback.message.edit_text(
#             response_text, reply_markup=get_main_menu_keyboard(lang))
#     else:
#         response_text = await text_service.get_text('select_your_course', lang)
#         await callback.message.edit_text(
#             response_text,
#             reply_markup=await get_student_courses_keyboard(
#                 student_courses, lang)
#         )
#     await state.update_data(current_student_course_id=None)
#     await callback.answer()
#     logger.info(f"Пользователь {callback.from_user.id} возвращен в список курсов для студентов. Язык: {lang}.")
