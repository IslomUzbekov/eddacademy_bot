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
            self.texts.clear()

            bot_texts = BotText.objects.all()
            for text_obj in bot_texts:
                self.texts[text_obj.key] = {
                    'en': text_obj.en,
                    'ru': text_obj.ru,
                    'uz': text_obj.uz,
                }
            self.is_loaded = True
            logger.info("Тексты бота успешно загружены из базы данных.")
        except Exception as e:
            logger.error(f"Не удалось загрузить тексты бота из базы данных: {e}")
            self.is_loaded = False

    async def get_text(self, key: str, lang_code: str, **kwargs) -> str:
        """
        Возвращает текст по ключу и языку, с возможностью форматирования.
        Автоматически загружает тексты, если они еще не загружены.
        """

        if not self.is_loaded:
            await self._load_texts_from_db()
            if not self.is_loaded:
                logger.warning(
                    f"Тексты не загружаются. Возвращение обратного хода для ключа '{key}'"
                    )
                return f"Текст для ключа '{key}' не найден или загрузка не удалась."

        text_data = self.texts.get(key)
        if not text_data:
            logger.warning(f"Текстовый ключ '{key}' не найден в загруженных текстах.")
            return f"Текст для ключа '{key}' не найден."

        text = text_data.get(lang_code)
        if not text:
            text = text_data.get(
                'en', f"Текст для ключа '{key}' не найден для '{lang_code}'."
                )
            logger.warning(
                f"Нет перевода для ключа '{key}' в '{lang_code}', возвращаемся к английскому"
                )

        try:
            return text.format(**kwargs)
        except KeyError as e:
            logger.error(
                f"Отсутствует заполнитель '{e}' в тексте для ключа '{key}' ({
                    lang_code}). Text: '{text}'"
                )
            return text + f" (Ошибка форматирования: Отсутствует '{e}')"
        except Exception as e:
            logger.error(
                f"Ошибка форматирования текста для ключа '{key}' ({
                    lang_code}): {e}. Text: '{text}'"
                )
            return text + f" (Ошибка форматирования: {e})"

    @sync_to_async
    def get_all_translations(self, key: str) -> List[str]:
        """
        Получает все доступные переводы для данного ключа.
        Возвращает список строк.
        """

        text_data = self.texts.get(key)
        if not text_data:
            logger.warning(f"Для ключа не найдено ни одного перевода '{key}'.")
            return []

        return list(text_data.values())


# Создаем единственный экземпляр сервиса
text_service = TextService()
