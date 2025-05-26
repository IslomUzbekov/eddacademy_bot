# your_telegram_bot_project/telegram_bot/management/commands/runbot.py

import asyncio
import logging

from django.core.management.base import BaseCommand

# Конфигурация логирования (опционально, но полезно)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Runs the Telegram bot'

    def handle(self, *args, **options):
        # Запуск асинхронной функции бота
        # Мы импортируем main и его функцию main() здесь,
        # чтобы убедиться, что Django-окружение уже инициализировано.
        from bot.main import main
        logger.info("Starting Telegram bot...")
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Bot stopped by user.")
        except Exception as e:
            logger.error(f"Error running bot: {e}")
