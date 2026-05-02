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
        'price',
        'discount_percentage',
        'is_active',
        'created_at'
    )
    list_filter = ('is_active', 'category', 'speaker',)
    list_editable = ('price', 'discount_percentage', 'is_active',)
    search_fields = (
        'title_en', 'title_ru', 'title_uz',
        'description_en', 'description_ru', 'description_uz'
    )
    readonly_fields = ('created_at', 'updated_at',)
    fieldsets = (
        (None, {
            'fields': (
                'category',
                'speaker',
                'image',
                'price',
                'discount_percentage',
                'rating',
                'duration_months',
                'is_active'
            )
        }),
        (_("Localized Titles"), {
            'fields': ('title_en', 'title_ru', 'title_uz',),
            'classes': ('collapse',),
        }),
        (_("Localized Descriptions"), {
            'fields': ('description_en', 'description_ru', 'description_uz',),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('created_at', 'updated_at',)
        }),
    )
    ordering = ('title_en',)


# --- CourseCategory Admin ---
@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ru', 'name_uz', 'slug', 'is_active', 'order',)
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order',)
    search_fields = ('name_en', 'name_ru', 'name_uz', 'description_en', 'description_ru', 'description_uz',)
    prepopulated_fields = {'slug': ('name_en',)}
    fieldsets = (
        (None, {
            'fields': ('name_en', 'slug', 'is_active', 'order',)
        }),
        (_("Localized Names"), {
            'fields': ('name_ru', 'name_uz',),
            'classes': ('collapse',),
        }),
        (_("Localized Descriptions"), {
            'fields': ('description_en', 'description_ru', 'description_uz',),
            'classes': ('collapse',),
        }),
    )
    ordering = ('order',)


# --- FAQItem Admin ---
@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question_en', 'is_active', 'order', 'created_at',)
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order',)
    search_fields = (
        'question_en', 'answer_en',
        'question_ru', 'answer_ru',
        'question_uz', 'answer_uz'
    )
    readonly_fields = ('created_at', 'updated_at',)
    fieldsets = (
        (None, {
            'fields': ('order', 'is_active')
        }),
        (_("Question and Answer (English)"), {
            'fields': ('question_en', 'answer_en',)
        }),
        (_("Question and Answer (Russian)"), {
            'fields': ('question_ru', 'answer_ru',),
            'classes': ('collapse',),
        }),
        (_("Question and Answer (Uzbek)"), {
            'fields': ('question_uz', 'answer_uz',),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('created_at', 'updated_at',)
        }),
    )
    ordering = ('order',)


# --- BotText Admin ---
@admin.register(BotText)
class BotTextAdmin(admin.ModelAdmin):
    list_display = ('key', 'en', 'ru', 'uz',)
    search_fields = ('key', 'en', 'ru', 'uz',)
    fieldsets = (
        (None, {
            'fields': ('key',)
        }),
        (_("Localized Texts"), {
            'fields': ('en', 'ru', 'uz',),
        }),
    )
    ordering = ('key',)


# --- NewsItem Admin ---
@admin.register(NewsItem)
class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'published_date', 'is_active', 'created_at',)
    list_filter = ('is_active',)
    search_fields = (
        'title_en', 'text_en',
        'title_ru', 'text_ru',
        'title_uz', 'text_uz'
    )
    readonly_fields = ('created_at', 'updated_at',)
    fieldsets = (
        (None, {
            'fields': ('image', 'telegram_channel_link', 'published_date', 'is_active')
        }),
        (_("Localized Titles"), {
            'fields': ('title_en', 'title_ru', 'title_uz'),
            'classes': ('collapse',),
        }),
        (_("Localized Texts"), {
            'fields': ('text_en', 'text_ru', 'text_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('created_at', 'updated_at',)
        }),
    )
    ordering = ('-published_date',)


# --- Speaker Admin ---
@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ru', 'name_uz', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name_en', 'name_ru', 'name_uz', 'bio_en', 'bio_ru', 'bio_uz',)
    fieldsets = (
        (None, {
            'fields': ('photo', 'is_active')
        }),
        (_("Localized Names"), {
            'fields': ('name_en', 'name_ru', 'name_uz'),
            'classes': ('collapse',),
        }),
        (_("Localized Bios"), {
            'fields': ('bio_en', 'bio_ru', 'bio_uz'),
            'classes': ('collapse',),
        }),
    )
    ordering = ('name_en',)


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
    list_filter = ('is_active', 'speaker',)
    search_fields = (
        'title_en', 'description_en',
        'title_ru', 'description_ru',
        'title_uz', 'description_uz',
        'location_or_link'
    )
    readonly_fields = ('created_at', 'updated_at',)
    fieldsets = (
        (None, {
            'fields': (
                'speaker',
                'lesson_date',
                'start_time',
                'end_time',
                'online_meeting_url',
                'location_or_link',
                'is_active'
            )
        }),
        (_("Localized Titles"), {
            'fields': ('title_en', 'title_ru', 'title_uz'),
            'classes': ('collapse',),
        }),
        (_("Localized Descriptions"), {
            'fields': ('description_en', 'description_ru', 'description_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('created_at', 'updated_at',)
        }),
    )
    ordering = ('lesson_date', 'start_time',)


# --- Student Admin ---
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'student_id_number',
        'telegram_user',
        'is_active',
        'enrollment_date'
    )
    list_filter = ('is_active', 'enrollment_date',)
    search_fields = ('full_name', 'student_id_number', 'telegram_user__username', 'telegram_user__user_id',)
    filter_horizontal = ('enrolled_courses',) # Для удобного выбора курсов
    readonly_fields = ('enrollment_date', 'created_at', 'updated_at',)
    fieldsets = (
        (None, {
            'fields': (
                'telegram_user',
                'full_name',
                'student_id_number',
                'date_of_birth',
                'is_active',
            )
        }),
        (_("Courses"), {
            'fields': ('enrolled_courses',),
        }),
        (None, {
            'fields': ('enrollment_date', 'created_at', 'updated_at',)
        }),
    )
    ordering = ('full_name',)


# --- StudentApplication Admin ---
@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'phone_number',
        'course',
        'status',
        'applied_at',
        'updated_at'
    )
    list_filter = ('status', 'course',)
    list_editable = ('status',)
    search_fields = ('full_name', 'phone_number', 'email', 'telegram_user__username',)
    readonly_fields = ('applied_at', 'updated_at',)
    fieldsets = (
        (None, {
            'fields': (
                'telegram_user',
                'full_name',
                'phone_number',
                'email',
                'course',
                'status',
                'admin_notes'
            )
        }),
        (None, {
            'fields': ('applied_at', 'updated_at',)
        }),
    )
    ordering = ('-applied_at',)


# --- Grade Admin ---
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'course',
        'score',
        'grade_date',
        'graded_by',
    )
    list_filter = ('course', 'graded_by', 'grade_date',)
    list_editable = ('score',)
    search_fields = (
        'student__full_name',
        'course__title_en',
        'lesson_topic_en',
        'notes'
    )
    fieldsets = (
        (None, {
            'fields': (
                'student',
                'course',
                'score',
                'grade_date',
                'graded_by',
                'notes'
            )
        }),
        (_("Localized Lesson Topic"), {
            'fields': ('lesson_topic_en', 'lesson_topic_ru', 'lesson_topic_uz',),
            'classes': ('collapse',),
        }),
    )
    ordering = ('-grade_date', 'student__full_name',)


# --- ScheduleItem Admin ---
@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'title_en',
        'lesson_date',
        'lesson_time',
        'is_active',
    )
    list_filter = ('course', 'is_active',)
    list_editable = ('is_active',)
    search_fields = (
        'title_en', 'description_en',
        'title_ru', 'description_ru',
        'title_uz', 'description_uz',
    )
    fieldsets = (
        (None, {
            'fields': (
                'course',
                'lesson_date',
                'lesson_time',
                'is_active',
            )
        }),
        (_("Localized Titles"), {
            'fields': ('title_en', 'title_ru', 'title_uz'),
            'classes': ('collapse',),
        }),
        (_("Localized Descriptions"), {
            'fields': ('description_en', 'description_ru', 'description_uz'),
            'classes': ('collapse',),
        }),
    )
    ordering = ['lesson_date', 'lesson_time']


# --- CourseMaterial Admin ---
@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = (
        'course',
        'title_en',
        'url',
        'order',
    )
    list_filter = ('course',)
    list_editable = ('order',)
    search_fields = (
        'title_en', 'description_en',
        'title_ru', 'description_ru',
        'title_uz', 'description_uz',
        'url'
    )
    fieldsets = (
        (None, {
            'fields': (
                'course',
                'url',
                'order'
            )
        }),
        (_("Localized Titles"), {
            'fields': ('title_en', 'title_ru', 'title_uz'),
            'classes': ('collapse',),
        }),
        (_("Localized Descriptions"), {
            'fields': ('description_en', 'description_ru', 'description_uz'),
            'classes': ('collapse',),
        }),
    )
    ordering = ('course__title_en', 'order',)


# --- AboutUsHistory Admin ---
@admin.register(AboutUsHistory)
class AboutUsHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'title_en',
        'title_ru',
        'title_uz',
        'updated_at'
    )
    search_fields = ('title_en', 'title_ru', 'title_uz', 'content_en', 'content_ru', 'content_uz')
    readonly_fields = ('updated_at',)
    # list_filter и list_editable удалены, так как нет подходящих полей в текущей модели AboutUsHistory
    ordering = ('title_en', 'updated_at',) # Используем существующие поля для сортировки
    fieldsets = (
        (None, {
            'fields': ('title_en', 'title_ru', 'title_uz')
        }),
        (_("Content"), {
            'fields': ('content_en', 'content_ru', 'content_uz'),
            'classes': ('collapse',),
        }),
        (None, {
            'fields': ('updated_at',)
        }),
    )


# --- TeamMember Admin ---
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'position_en', 'order', 'is_active',)
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active',)
    search_fields = (
        'name_en', 'name_ru', 'name_uz',
        'position_en', 'position_ru', 'position_uz',
        'bio_en', 'bio_ru', 'bio_uz',
    )
    fieldsets = (
        (None, {
            'fields': ('photo', 'order', 'is_active')
        }),
        (_("Localized Names"), {
            'fields': ('name_en', 'name_ru', 'name_uz'),
            'classes': ('collapse',),
        }),
        (_("Localized Positions"), {
            'fields': ('position_en', 'position_ru', 'position_uz'),
            'classes': ('collapse',),
        }),
        (_("Localized Biographies"), {
            'fields': ('bio_en', 'bio_ru', 'bio_uz'),
            'classes': ('collapse',),
        }),
    )
    ordering = ('order', 'name_en',)


# --- Partner Admin ---
@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'order', 'is_active',)
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active',)
    search_fields = ('name', 'description_en', 'description_ru', 'description_uz', 'website_url',)
    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'website_url', 'order', 'is_active',)
        }),
        (_("Localized Descriptions"), {
            'fields': ('description_en', 'description_ru', 'description_uz',),
            'classes': ('collapse',),
        }),
    )
    ordering = ('order', 'name',)


# --- Achievement Admin ---
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'date', 'order', 'is_active',)
    list_filter = ('is_active',)
    list_editable = ('order', 'is_active',)
    search_fields = (
        'title_en', 'description_en',
        'title_ru', 'description_ru',
        'title_uz', 'description_uz',
    )
    fieldsets = (
        (None, {
            'fields': ('image', 'date', 'order', 'is_active')
        }),
        (_("Localized Titles"), {
            'fields': ('title_en', 'title_ru', 'title_uz'),
            'classes': ('collapse',),
        }),
        (_("Localized Descriptions"), {
            'fields': ('description_en', 'description_ru', 'description_uz'),
            'classes': ('collapse',),
        }),
    )
    ordering = ('-date', 'order',)


# --- Review Admin ---
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'is_approved', 'created_at',)
    list_filter = ('is_approved', 'rating',)
    list_editable = ('is_approved',)
    search_fields = ('author_name', 'review_text_en', 'review_text_ru', 'review_text_uz',)
    readonly_fields = ('created_at',)
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
