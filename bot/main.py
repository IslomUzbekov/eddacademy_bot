# your_telegram_bot_project/bot/main.py

import logging
import os

import django
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from bot.bot_instance import bot, dp

# Импортируем все роутеры (хэндлеры)
from bot.handlers import (
    admin,
    common,
    courses,
    # faq,
    # registration,
)

# from bot.services.application_service import application_service
from bot.services.course_service import course_service

# from bot.services.faq_service import faq_service
from bot.services.text_service import text_service
from bot.services.user_service import user_service

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


async def set_default_commands(bot_instance: Bot):
    """
    Устанавливает стандартные команды для бота.
    """

    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="menu", description="Show main menu"),
        BotCommand(command="faq", description="Frequently asked questions"),
        BotCommand(command="help", description="Get help"),
    ]
    await bot_instance.set_my_commands(commands)


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    """
    Вызывается при старте бота.
    Загружает тексты из БД и устанавливает команды.
    """

    logging.info("Bot started successfully!")
    await set_default_commands(bot)
    await text_service._load_texts_from_db()
    logging.info("Bot texts loaded.")


async def on_shutdown(dispatcher: Dispatcher):
    """
    Вызывается при остановке бота.
    """
    logging.info("Bot is shutting down.")


def setup_routers(dispatcher: Dispatcher):
    """
    Регистрирует все роутеры в диспетчере.
    Порядок имеет значение для обработки сообщений
    (первый зарегистрированный имеет приоритет).
    """

    # Хэндлеры для курсов и записи
    dispatcher.include_router(courses.router)
    # dispatcher.include_router(registration.router)
    # Хэндлеры для FAQ
    # dispatcher.include_router(faq.router)
    # Админ-хэндлеры (если есть)
    dispatcher.include_router(admin.router)
    # Общие хэндлеры (start, help, menu, выбор языка)
    dispatcher.include_router(common.router)


def main():
    """
    Главная функция для запуска бота.
    """

    dp.workflow_data.update({
        "user_service": user_service,
        "course_service": course_service,
        # "application_service": application_service,
        # "faq_service": faq_service,
        "text_service": text_service,
    })

    # Регистрируем функции запуска и остановки
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Настраиваем роутеры
    setup_routers(dp)

    # Запускаем опрос новых обновлений от Telegram
    dp.run_polling(bot)


if __name__ == '__main__':
    # Настраиваем базовое логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
        )
    main()
