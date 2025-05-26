# your_telegram_bot_project/telegram_bot/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    AboutUsHistory,
    Achievement,
    BotText,
    ContactInfo,
    Course,
    CourseCategory,
    CourseMaterial,
    FAQItem,
    Grade,
    NewsItem,
    OpenLesson,
    Partner,
    Review,
    ScheduleItem,
    Speaker,
    Student,
    StudentApplication,
    TeamMember,
    TelegramUser,
)


# --- TelegramUser Admin ---
@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id',
        'username',
        'first_name',
        'last_name',
        'language_code',
        'is_admin',
        'created_at',
        'updated_at'
    )
    search_fields = ('user_id', 'username', 'first_name', 'last_name')
    readonly_fields = ('user_id', 'created_at', 'updated_at')
    list_filter = ('is_bot', 'language_code', 'is_admin')
    ordering = ('-created_at',)


# --- Course Admin ---
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'title_en',
        'category',
        'duration_months',
        'price',
        'discount_percentage',
        'get_final_price_display',
        'is_active',
        'created_at'
    )
    list_filter = ('is_active', 'category')
    search_fields = (
        'title_en', 'description_en',
        'title_ru', 'description_ru',
        'title_uz', 'description_uz'
    )
    ordering = ('title_en',)
    fieldsets = (
        (_("English Content"), {
            'fields': ('title_en', 'description_en')
        }),
        (_("Russian Content"), {
            'fields': ('title_ru', 'description_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('title_uz', 'description_uz'),
            'classes': ('collapse',),
        }),
        (_("Course Details"), {
            'fields': (
                'category',
                'duration_months',
                'price',
                'discount_percentage',
                'image',
                'is_active'
            )
        }),
    )

    def get_final_price_display(self, obj):
        return f"{obj.get_final_price():.2f}"
    get_final_price_display.short_description = _("Final Price")
    get_final_price_display.admin_order_field = 'price'


# --- CourseCategory Admin ---
@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name_en', 'name_ru', 'name_uz',
        'slug', 'is_active', 'order'
    )
    search_fields = ('name_en', 'name_ru', 'name_uz', 'slug')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name_en',)}
    ordering = ('order',)
    fieldsets = (
        (_("English Content"), {
            'fields': ('name_en', 'description_en')
        }),
        (_("Russian Content"), {
            'fields': ('name_ru', 'description_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('name_uz', 'description_uz'),
            'classes': ('collapse',),
        }),
        (_("Settings"), {
            'fields': ('slug', 'is_active', 'order')
        }),
    )


# --- StudentApplication Admin ---
@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone_number',
        'email',
        'course',
        'status',
        'applied_at'
    )
    list_filter = ('status', 'course', 'applied_at')
    search_fields = (
        'full_name',
        'phone_number',
        'email',
        'admin_notes',
        'telegram_user__username',
        'course__title_en'
    )
    readonly_fields = ('telegram_user', 'applied_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': (
                'telegram_user',
                'full_name',
                'phone_number',
                'email',
                'course',
                'status'
            )
        }),
        (_("Admin Information"), {
            'fields': ('admin_notes',),
            'classes': ('collapse',)
        }),
        (_("Timestamps"), {
            'fields': ('applied_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-applied_at',)


# --- FAQItem Admin ---
@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question_en', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = (
        'question_en', 'answer_en',
        'question_ru', 'answer_ru',
        'question_uz', 'answer_uz'
    )
    ordering = ('order', 'question_en')
    fieldsets = (
        (_("English Content"), {
            'fields': ('question_en', 'answer_en')
        }),
        (_("Russian Content"), {
            'fields': ('question_ru', 'answer_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('question_uz', 'answer_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('order', 'is_active')
        }),
    )


# --- BotText Admin ---
@admin.register(BotText)
class BotTextAdmin(admin.ModelAdmin):
    list_display = ('key', 'en', 'ru', 'uz')
    search_fields = ('key', 'en', 'ru', 'uz')
    # Используем fieldsets для лучшей организации
    fieldsets = (
        (None, {
            'fields': ('key',)
        }),
        (_("Localized Texts"), {
            'fields': ('en', 'ru', 'uz')
        }),
    )


# --- NewsItem Admin ---
@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'published_date', 'is_active', 'created_at')
    list_filter = ('is_active', 'published_date')
    search_fields = (
        'title_en', 'text_en',
        'title_ru', 'text_ru',
        'title_uz', 'text_uz'
    )
    ordering = ('-published_date',)
    fieldsets = (
        (_("English Content"), {
            'fields': ('title_en', 'text_en', 'image')
        }),
        (_("Russian Content"), {
            'fields': ('title_ru', 'text_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('title_uz', 'text_uz'),
            'classes': ('collapse',),
        }),
        (_("Additional Info"), {
            'fields': ('telegram_channel_link', 'published_date', 'is_active')
        }),
    )


# --- Speaker Admin ---
@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'bio_en', 'is_active')
    list_filter = ('is_active',)
    search_fields = (
        'name_en', 'bio_en', 'name_ru', 'bio_ru', 'name_uz', 'bio_uz'
        )
    ordering = ('name_en',)
    fieldsets = (
        (_("English Content"), {
            'fields': ('name_en', 'bio_en')
        }),
        (_("Russian Content"), {
            'fields': ('name_ru', 'bio_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('name_uz', 'bio_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('photo', 'is_active')
        }),
    )


# --- OpenLesson Admin ---
@admin.register(OpenLesson)
class OpenLessonAdmin(admin.ModelAdmin):
    list_display = (
        'title_en',
        'lesson_date',
        'start_time',
        'speaker',
        'is_active',
        'created_at'
    )
    list_filter = ('is_active', 'lesson_date', 'speaker')
    search_fields = (
        'title_en', 'description_en', 'location_or_link',
        'title_ru', 'description_ru',
        'title_uz', 'description_uz',
        'speaker__name_en'
    )
    ordering = ('lesson_date', 'start_time')
    fieldsets = (
        (_("English Content"), {
            'fields': ('title_en', 'description_en')
        }),
        (_("Russian Content"), {
            'fields': ('title_ru', 'description_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('title_uz', 'description_uz'),
            'classes': ('collapse',),
        }),
        (_("Lesson Details"), {
            'fields': (
                'lesson_date',
                ('start_time', 'end_time'),
                'speaker',
                'location_or_link',
                'is_active'
            )
        }),
    )


# --- Student Admin ---
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'student_id_number',
        'get_telegram_username',
        'is_active',
        'enrollment_date'
        )
    list_filter = ('is_active', 'enrollment_date', 'courses')
    search_fields = (
        'full_name',
        'student_id_number',
        'telegram_user__username',
        'telegram_user__user_id'
        )
    raw_id_fields = ('telegram_user',)
    filter_horizontal = ('courses',)
    ordering = ('full_name',)
    fieldsets = (
        (None, {
            'fields': (
                'telegram_user',
                'full_name',
                'student_id_number',
                'date_of_birth',
                'is_active'
                )
        }),
        (_("Courses and Dates"), {
            'fields': ('courses', 'enrollment_date')
        }),
    )

    def get_telegram_username(self, obj):
        return obj.telegram_user.username if obj.telegram_user else _("N/A")
    get_telegram_username.short_description = _("Telegram Username")


# --- Grade Admin ---
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course',
        'get_localized_lesson_topic_display',
        'score',
        'grade_date'
        )
    list_filter = ('course', 'grade_date')
    search_fields = (
        'student__full_name',
        'course__title_en',
        'lesson_topic_en',
        'notes'
        )
    ordering = ('-grade_date', 'student__full_name')
    fieldsets = (
        (None, {
            'fields': ('student', 'course', 'score', 'grade_date', 'notes')
        }),
        (_("Lesson Topic (Localized)"), {
            'fields': (
                'lesson_topic_en',
                'lesson_topic_ru',
                'lesson_topic_uz'
                ),
            'classes': ('collapse',)
        }),
    )

    def get_localized_lesson_topic_display(self, obj):
        return obj.get_localized_lesson_topic(
            self.request.user.language_code if hasattr(
                self.request.user,
                'language_code'
                ) else 'en'
            )
    get_localized_lesson_topic_display.short_description = _("Lesson Topic")


# --- ScheduleItem Admin ---
@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = (
        'course', 'title_en', 'lesson_date', 'lesson_time', 'is_active'
    )
    list_filter = ('is_active', 'course', 'lesson_date')
    search_fields = (
        'course__title_en',
        'title_en', 'description_en',
        'title_ru', 'description_ru',
        'title_uz', 'description_uz'
    )
    ordering = ('lesson_date', 'lesson_time', 'course__title_en')
    fieldsets = (
        (None, {
            'fields': ('course', ('lesson_date', 'lesson_time'), 'is_active')
        }),
        (_("English Content"), {
            'fields': ('title_en', 'description_en')
        }),
        (_("Russian Content"), {
            'fields': ('title_ru', 'description_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('title_uz', 'description_uz'),
            'classes': ('collapse',),
        }),
    )


# --- CourseMaterial Admin ---
@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ('course', 'title_en', 'url')
    list_filter = ('course',)
    search_fields = (
        'title_en', 'description_en', 'course__title_en', 'url',
        'title_ru', 'description_ru',
        'title_uz', 'description_uz'
    )
    ordering = ('course__title_en', 'title_en')
    fieldsets = (
        (None, {
            'fields': ('course', 'url')
        }),
        (_("English Content"), {
            'fields': ('title_en', 'description_en')
        }),
        (_("Russian Content"), {
            'fields': ('title_ru', 'description_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('title_uz', 'description_uz'),
            'classes': ('collapse',),
        }),
    )


# --- AboutUsHistory Admin (НОВАЯ МОДЕЛЬ) ---
@admin.register(AboutUsHistory)
class AboutUsHistoryAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'updated_at')
    readonly_fields = ('updated_at',)
    fieldsets = (
        (_("English Content"), {
            'fields': ('title_en', 'content_en')
        }),
        (_("Russian Content"), {
            'fields': ('title_ru', 'content_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('title_uz', 'content_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('updated_at',)
        }),
    )

    def has_add_permission(self, request):
        return not AboutUsHistory.objects.exists()


# --- TeamMember Admin ---
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'position_en', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name_en', 'position_en', 'bio_en')
    ordering = ('order', 'name_en')
    fieldsets = (
        (_("English Content"), {
            'fields': ('name_en', 'position_en', 'bio_en')
        }),
        (_("Russian Content"), {
            'fields': ('name_ru', 'position_ru', 'bio_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('name_uz', 'position_uz', 'bio_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('photo', 'order', 'is_active')
        }),
    )


# --- Partner Admin ---
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description_en', 'website_url')
    ordering = ('order', 'name')
    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'website_url')
        }),
        (_("Localized Description"), {
            'fields': ('description_en', 'description_ru', 'description_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('order', 'is_active')
        }),
    )


# --- Achievement Admin ---
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'date', 'order', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('title_en', 'description_en')
    ordering = ('-date', 'order')
    fieldsets = (
        (_("English Content"), {
            'fields': ('title_en', 'description_en')
        }),
        (_("Russian Content"), {
            'fields': ('title_ru', 'description_ru'),
            'classes': ('collapse',),
        }),
        (_("Uzbek Content"), {
            'fields': ('title_uz', 'description_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('image', 'date', 'order', 'is_active')
        }),
    )


# --- Review Admin ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating')
    search_fields = (
        'author_name',
        'review_text_en',
        'review_text_ru',
        'review_text_uz'
        )
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('author_name', 'rating', 'is_approved')
        }),
        (_("Localized Review Text"), {
            'fields': ('review_text_en', 'review_text_ru', 'review_text_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ('created_at',)


# --- ContactInfo Admin ---
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'email', 'website_url', 'updated_at')
    readonly_fields = ('updated_at',)
    fieldsets = (
        (_("General Contacts"), {
            'fields': ('phone_number', 'email', 'website_url', 'map_url')
        }),
        (_("Social Media Links"), {
            'fields': (
                'telegram_channel_url',
                'instagram_url',
                'facebook_url',
                'youtube_url'
                ),
            'classes': ('collapse',),
        }),
        (_("Localized Address"), {
            'fields': ('address_en', 'address_ru', 'address_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('updated_at',)
        }),
    )

    # Обычно ContactInfo это Singleton - одна запись
    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
