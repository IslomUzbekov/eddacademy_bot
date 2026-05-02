# bot/services/about_us_service.py

from asgiref.sync import sync_to_async
from telegram_bot.models import (
    AboutUsHistory, TeamMember, Partner, Achievement, Review
)


class AboutUsService:
    """
    Сервис для получения информации о разделе 'О нас'.
    """

    @sync_to_async
    def get_history(self, lang):
        # Берём последнюю запись (или нужную по логике)
        history = AboutUsHistory.objects.order_by('-updated_at').first()
        if not history:
            return "История не найдена."
        title = getattr(history, f"title_{lang}", history.title_en)
        content = getattr(history, f"content_{lang}", history.content_en)
        return f"<b>{title}</b>\n\n{content}"

    @sync_to_async
    def get_teachers(self, lang):
        members = TeamMember.objects.filter(is_active=True).order_by('order')
        if not members:
            return "Преподаватели не найдены."
        result = []
        for m in members:
            name = m.get_localized_name(lang)
            position = m.get_localized_position(lang)
            bio = m.get_localized_bio(lang)
            result.append(f"<b>{name}</b>\n{position}\n{bio}\n")
        return "\n".join(result)

    @sync_to_async
    def get_partners(self, lang):
        partners = Partner.objects.filter(is_active=True).order_by('order')
        if not partners:
            return "Партнёры не найдены."
        result = []
        for p in partners:
            desc = p.get_localized_description(lang)
            result.append(f"<b>{p.name}</b>\n{desc or ''}\n")
        return "\n".join(result)

    @sync_to_async
    def get_achievements(self, lang):
        achievements = Achievement.objects.filter(is_active=True).order_by('-date', 'order')
        if not achievements:
            return "Достижения не найдены."
        result = []
        for a in achievements:
            title = a.get_localized_title(lang)
            desc = a.get_localized_description(lang)
            result.append(f"<b>{title}</b>\n{desc or ''}\n")
        return "\n".join(result)

    @sync_to_async
    def get_reviews(self, lang):
        reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:10]
        if not reviews:
            return "Отзывы не найдены."
        result = []
        for r in reviews:
            text = r.get_localized_review_text(lang)
            result.append(f"⭐️ {r.rating}/5 — <b>{r.author_name}</b>\n{text}\n")
        return "\n".join(result)


# Экземпляр сервиса
about_us_service = AboutUsService()
