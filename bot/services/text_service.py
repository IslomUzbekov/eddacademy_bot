# bot/services/text_service.py

import logging
from typing import List

from asgiref.sync import sync_to_async
from telegram_bot.models import BotText

logger = logging.getLogger(__name__)


class TextService:
    def __init__(self):
        self.texts = {}
        self.is_loaded = False

    @sync_to_async
    def _load_texts_from_db(self):
        """
        Загружает все тексты из базы данных.
        """

        try:
            # Очищаем кэш перед загрузкой
            self.texts.clear()

            bot_texts = BotText.objects.all()
            for text_obj in bot_texts:
                self.texts[text_obj.key] = {
                    'en': text_obj.en,
                    'ru': text_obj.ru,
                    'uz': text_obj.uz,
                }
            self.is_loaded = True
            logger.info("Bot texts loaded successfully from database.")
        except Exception as e:
            logger.error(f"Failed to load bot texts from database: {e}")
            self.is_loaded = False

    async def get_text(self, key: str, lang_code: str, **kwargs) -> str:
        """
        Возвращает текст по ключу и языку, с возможностью форматирования.
        Автоматически загружает тексты, если они еще не загружены.
        """

        if not self.is_loaded:
            await self._load_texts_from_db()
            if not self.is_loaded:  # Если загрузка всё равно не удалась
                logger.warning(
                    f"Texts not loaded. Returning fallback for key '{key}'"
                    )
                return f"Text for key '{key}' not found or loading failed."

        text_data = self.texts.get(key)
        if not text_data:
            logger.warning(f"Text key '{key}' not found in loaded texts.")
            return f"Text for key '{key}' not found."

        text = text_data.get(lang_code)
        if not text:
            # Fallback к английскому, если перевода на нужный язык нет
            text = text_data.get(
                'en', f"Text for key '{key}' not found for '{lang_code}'."
                )
            logger.warning(
                f"No translation for key '{key}' in '{
                    lang_code}', falling back to English."
                )

        # Форматирование текста с помощью kwargs
        try:
            return text.format(**kwargs)
        except KeyError as e:
            logger.error(
                f"Missing placeholder '{e}' in text for key '{key}' ({
                    lang_code}). Text: '{text}'"
                )
            return text + f" (Formatting error: Missing '{e}')"
        except Exception as e:
            logger.error(
                f"Error formatting text for key '{key}' ({
                    lang_code}): {e}. Text: '{text}'"
                )
            return text + f" (Formatting error: {e})"

    @sync_to_async
    def get_all_translations(self, key: str) -> List[str]:
        """
        Получает все доступные переводы для данного ключа.
        Возвращает список строк.
        """

        text_data = self.texts.get(key)
        if not text_data:
            logger.warning(f"No translations found for key '{key}'.")
            return []

        # Возвращаем список значений из словаря переводов для данного ключа
        return list(text_data.values())


# Создаем единственный экземпляр сервиса
text_service = TextService()
