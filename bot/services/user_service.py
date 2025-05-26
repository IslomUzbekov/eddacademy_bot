# your_telegram_bot_project/bot/services/user_service.py

import logging
from django.conf import settings

from asgiref.sync import sync_to_async
from telegram_bot.models import TelegramUser

logger = logging.getLogger(__name__)


class UserService:
    @sync_to_async
    def get_or_create_user(
        self,
        user_id: int,
        username: str | None,
        first_name: str | None,
        last_name: str | None,
        is_bot: bool) -> tuple[TelegramUser, bool]:
        """
        Получает или создает пользователя Telegram.
        Если пользователь существует, обновляет его базовые данные
        (кроме языка).
        """

        user, created = TelegramUser.objects.get_or_create(
            user_id=user_id,
            defaults={
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'language_code': settings.DEFAULT_LANGUAGE, # Устанавливаем язык по умолчанию
                'is_bot': is_bot
            }
        )
        if not created:
            # Обновляем данные пользователя, если они изменились
            updated = False
            if user.username != username:
                user.username = username
                updated = True
            if user.first_name != first_name:
                user.first_name = first_name
                updated = True
            if user.last_name != last_name:
                user.last_name = last_name
                updated = True
            if user.is_bot != is_bot:
                user.is_bot = is_bot
                updated = True
            if updated:
                user.save()
                logger.info(f"User {user_id} updated: {user.username or user.first_name}")

        logger.info(f"User {user_id} {'created' if created else 'retrieved'}. Current language in DB: {user.language_code}")
        return user, created

    @sync_to_async
    def get_user_by_id(self, user_id: int) -> TelegramUser | None:
        """
        Получает пользователя Telegram по его ID.
        """
        try:
            return TelegramUser.objects.get(user_id=user_id)
        except TelegramUser.DoesNotExist:
            logger.warning(f"User with ID {user_id} not found.")
            return None

    @sync_to_async
    def save_user(self, user: TelegramUser) -> None:
        """
        Сохраняет изменения в объекте пользователя.
        """
        user.save()

    @sync_to_async
    def set_user_language(self, user_id: int, language_code: str) -> bool:
        """
        Устанавливает язык для существующего пользователя.
        Возвращает True, если язык успешно обновлен, False в противном случае.
        """
        try:
            user = TelegramUser.objects.get(user_id=user_id)
            user.language_code = language_code
            user.save()
            logger.info(f"User {user_id} language updated to {language_code}.")
            return True
        except TelegramUser.DoesNotExist:
            logger.warning(f"Attempted to set language for non-existent user {user_id}.")
            return False
