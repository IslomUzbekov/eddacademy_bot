# # your_telegram_bot_project/bot/services/news_service.py

# import logging

# from asgiref.sync import sync_to_async
# from django.utils import timezone
# from telegram_bot.models import NewsItem

# logger = logging.getLogger(__name__)


# class NewsService:
#     @sync_to_async
#     def get_recent_news(self, days_ago: int = 30):
#         """
#         Возвращает активные новости, опубликованные за последние
#         `days_ago` дней, отсортированные по дате публикации
#         (от новых к старым).
#         """
#         # Получаем дату, начиная с которой ищем новости
#         min_date = timezone.now() - timezone.timedelta(days=days_ago)
#         try:
#             news = list(NewsItem.objects.filter(
#                 is_active=True,
#                 published_date__gte=min_date
#             ).order_by('-published_date'))
#             logger.debug(f"Извлечение {len(news)} последних новостей (активных и за последние {days_ago} дней).")
#             return news
#         except Exception as e:
#             logger.error(f"Ошибка при получении последних новостей: {e}")
#             return []


# # Создаем единственный экземпляр сервиса для использования во всем приложении
# news_service = NewsService()
