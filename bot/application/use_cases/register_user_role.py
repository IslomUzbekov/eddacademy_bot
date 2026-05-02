from django.conf import settings
from telegram_bot.models import TelegramUser

from bot.infrastructure.repositories.profile_repository import profile_repository
from bot.services.user_service import user_service


class RegisterUserRoleUseCase:
    async def set_regular_user_role(self, *, telegram_user_id: int) -> bool:
        return await user_service.set_user_role(telegram_user_id, TelegramUser.Role.USER)

    async def register_student_role(self, *, telegram_user_id: int, student_id: str) -> bool:
        return await profile_repository.bind_student_profile(
            telegram_user_id=telegram_user_id,
            student_id=student_id,
        )

    async def register_graduate_role(self, *, telegram_user_id: int, graduate_id: str) -> bool:
        return await profile_repository.bind_graduate_profile(
            telegram_user_id=telegram_user_id,
            graduate_id=graduate_id,
        )

    async def register_manager_role(self, *, telegram_user_id: int, code: str) -> bool:
        expected = getattr(settings, 'MANAGER_REGISTRATION_CODE', None)
        if not expected or code != expected:
            return False
        return await user_service.set_user_role(telegram_user_id, TelegramUser.Role.MANAGER)

    async def register_admin_role(self, *, telegram_user_id: int, code: str) -> bool:
        expected = getattr(settings, 'ADMIN_REGISTRATION_CODE', None)
        if not expected or code != expected:
            return False
        return await user_service.set_user_role(telegram_user_id, TelegramUser.Role.ADMIN)


register_user_role_use_case = RegisterUserRoleUseCase()
