# # bot/services/application_service.py
# from asgiref.sync import sync_to_async
# from telegram_bot.models import Course, StudentApplication, TelegramUser


# class ApplicationService:
#     """
#     Сервис для работы с заявками студентов.
#     Отвечает за создание и управление заявками.
#     """

#     @sync_to_async
#     def create_application(
#         self,
#         telegram_user: TelegramUser,
#         full_name: str,
#         phone_number: str,
#         course: Course,
#         email: str = None):
#         """
#         Создает новую заявку на курс.
#         """
#         application = StudentApplication.objects.create(
#             telegram_user=telegram_user,
#             full_name=full_name,
#             phone_number=phone_number,
#             email=email,
#             course=course,
#             status='new'
#         )
#         return application

#     @sync_to_async
#     def get_application_by_id(self, app_id: int):
#         """
#         Получает заявку по ID.
#         """
#         try:
#             return StudentApplication.objects.get(id=app_id)
#         except StudentApplication.DoesNotExist:
#             return None

#     @sync_to_async
#     def update_application_status(self, app_id: int, new_status: str):
#         """
#         Обновляет статус заявки.
#         """
#         application = self.get_application_by_id(app_id)
#         if application:
#             application.status = new_status
#             application.save()
#             return True
#         return False


# # Создаем единственный экземпляр сервиса
# application_service = ApplicationService()
