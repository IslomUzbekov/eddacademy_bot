# # your_telegram_bot_project/bot/services/faq_service.py

# from typing import Any, Dict, List

# from asgiref.sync import sync_to_async
# from telegram_bot.models import FAQItem


# class FaqService:
#     @sync_to_async
#     def get_active_faq_items(self, lang_code: str) -> List[Dict[str, str]]:
#         """
#         Возвращает список активных FAQ-элементов, отсортированных по 'order',
#         с вопросами и ответами на указанном языке.
#         """

#         faq_items = FAQItem.objects.filter(is_active=True).order_by('order')

#         result = []
#         for item in faq_items:
#             # Получаем вопрос и ответ на основе lang_code
#             question_field = f"question_{lang_code}"
#             answer_field = f"answer_{lang_code}"

#             question = getattr(item, question_field, getattr(
#                 item, 'question_en', 'N/A Question'
#                 ))
#             answer = getattr(item, answer_field, getattr(
#                 item, 'answer_en', 'N/A Answer'
#                 ))

#             result.append({
#                 'id': item.id,
#                 'question': question,
#                 'answer': answer
#             })
#         return result

#     @sync_to_async
#     def get_faq_item_by_id(self, faq_id: int, lang_code: str
#                            ) -> Dict[str, str] | None:
#         """
#         Возвращает конкретный FAQ-элемент по ID на указанном языке.
#         """

#         try:
#             item = FAQItem.objects.get(id=faq_id, is_active=True)
#             question_field = f"question_{lang_code}"
#             answer_field = f"answer_{lang_code}"

#             question = getattr(item, question_field, getattr(
#                 item, 'question_en', 'N/A Question'
#                 ))
#             answer = getattr(item, answer_field, getattr(
#                 item, 'answer_en', 'N/A Answer'
#                 ))

#             return {
#                 'id': item.id,
#                 'question': question,
#                 'answer': answer
#             }
#         except FAQItem.DoesNotExist:
#             return None


# # Создаем единственный экземпляр сервиса
# faq_service = FaqService()
