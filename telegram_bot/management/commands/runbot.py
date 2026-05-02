import asyncio
import logging

from django.core.management.base import BaseCommand

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Launches the Telegram bot'

    def handle(self, *args, **options):
        from bot.main import main
        logger.info("Starting Telegram bot...")
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            logger.info("Bot stopped by user.")
        except Exception as exc:
            logger.exception(f"Error while running the bot: {exc}")
