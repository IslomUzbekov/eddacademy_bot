from asgiref.sync import sync_to_async

from telegram_bot.models import Graduate, Student, TelegramUser


class ProfileRepository:
    @sync_to_async
    def bind_student_profile(self, *, telegram_user_id: int, student_id: str) -> bool:
        try:
            user = TelegramUser.objects.get(user_id=telegram_user_id)
            student = Student.objects.get(student_id_number=student_id, is_active=True)
        except (TelegramUser.DoesNotExist, Student.DoesNotExist):
            return False

        student.telegram_user = user
        student.save(update_fields=["telegram_user"])
        user.role = TelegramUser.Role.STUDENT
        user.save(update_fields=["role", "updated_at"])
        return True

    @sync_to_async
    def bind_graduate_profile(self, *, telegram_user_id: int, graduate_id: str) -> bool:
        try:
            user = TelegramUser.objects.get(user_id=telegram_user_id)
            graduate = Graduate.objects.get(
                graduate_id_number=graduate_id, is_active=True
            )
        except (TelegramUser.DoesNotExist, Graduate.DoesNotExist):
            return False

        graduate.telegram_user = user
        graduate.save(update_fields=["telegram_user"])
        user.role = TelegramUser.Role.GRADUATE
        user.save(update_fields=["role", "updated_at"])
        return True


profile_repository = ProfileRepository()
