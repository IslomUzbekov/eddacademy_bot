from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


# Модель для пользователя Telegram
class TelegramUser(models.Model):
    user_id = models.BigIntegerField(
        unique=True, db_index=True, verbose_name=_("Telegram User ID")
    )
    username = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Username")
    )
    first_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("First Name")
    )
    last_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("Last Name")
    )
    language_code = models.CharField(
        max_length=10,
        default='ru',
        null=True, blank=True,
        verbose_name=_("Language Code")
    )
    is_bot = models.BooleanField(
        default=False, verbose_name=_("Is Bot Account")
    )
    is_admin = models.BooleanField(
        default=False, verbose_name=_("Is Admin")
    )
    is_blocked = models.BooleanField(
        default=False, verbose_name=_("Is Blocked by User")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last Updated At")
    )

    def __str__(self):
        return f"{self.username or self.first_name} ({self.user_id})"

    class Meta:
        verbose_name = _("Telegram User")
        verbose_name_plural = _("Telegram Users")
        ordering = ['-created_at']


# Модель для категорий курсов
class CourseCategory(models.Model):
    name_en = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Category Name (English)"
    )
    name_ru = models.CharField(
        max_length=255,
        unique=True, blank=True, null=True,
        verbose_name="Category Name (Russian)"
    )
    name_uz = models.CharField(
        max_length=255,
        unique=True, blank=True, null=True,
        verbose_name="Category Name (Uzbek)"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True, blank=True, null=True,
        help_text=_("A unique slug generated from the English name.")
    )
    description_en = models.TextField(
        blank=True, null=True, verbose_name="Description (English)"
    )
    description_ru = models.TextField(
        blank=True, null=True, verbose_name="Description (Russian)"
    )
    description_uz = models.TextField(
        blank=True, null=True, verbose_name="Description (Uzbek)"
    )
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(
        default=0, help_text="Order in which categories are displayed."
    )

    class Meta:
        verbose_name = "Course Category"
        verbose_name_plural = "Course Categories"
        ordering = ['order']

    def __str__(self):
        return self.name_en

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_en)
        super().save(*args, **kwargs)

    def get_localized_name(self, lang_code: str) -> str:
        return getattr(self, f'name_{lang_code}', self.name_en)

    def get_localized_description(self, lang_code: str) -> str:
        return getattr(self, f'description_{lang_code}', self.description_en)


# Модель для курсов
class Course(models.Model):
    category = models.ForeignKey(
        'CourseCategory',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='courses',
        verbose_name=_("Category")
    )
    title_en = models.CharField(
        max_length=255, verbose_name=_("Course Title (English)")
    )
    description_en = models.TextField(verbose_name=_("Description (English)"))

    title_ru = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Course Title (Russian)")
    )
    description_ru = models.TextField(
        blank=True, null=True,
        verbose_name=_("Description (Russian)")
    )

    title_uz = models.CharField(
        blank=True, null=True,
        max_length=255, verbose_name=_("Course Title (Uzbek)")

    )
    description_uz = models.TextField(
        blank=True, null=True,
        verbose_name=_("Description (Uzbek)")
    )
    duration_months = models.IntegerField(
        default=1,
        verbose_name=_("Duration (Months)"),
        validators=[MinValueValidator(1)]
    )
    image = models.ImageField(
        upload_to='course_images/',
        null=True, blank=True,
        verbose_name=_("Course Image")
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name=_("Price"),
        validators=[MinValueValidator(0.00)]
    )
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00,
        verbose_name=_("Discount Percentage"),
        help_text=_("Percentage discount (e.g., 10.00 for 10%)"),
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)]
    )
    speaker = models.ForeignKey(
        'Speaker',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='courses_taught',
        verbose_name=_("Main Speaker")
    )
    rating = models.DecimalField(
        max_digits=3, decimal_places=2,
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name=_("Rating")
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_("Is Active")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last Updated At")
    )

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")
        ordering = ['title_en']

    def get_localized_title(self, lang_code: str) -> str:
        return getattr(self, f'title_{lang_code}', self.title_en)

    def get_localized_description(self, lang_code: str) -> str:
        return getattr(self, f'description_{lang_code}', self.description_en)

    def get_final_price(self) -> float:
        """Calculates the price after discount."""
        return float(self.price) * (1 - float(self.discount_percentage) / 100)


# Модель для заявок студентов
class StudentApplication(models.Model):
    STATUS_CHOICES = [
        ('new', _('New')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    telegram_user = models.ForeignKey(
        TelegramUser,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_("Telegram User")
    )
    full_name = models.CharField(
        max_length=255, verbose_name=_("Full Name")
    )
    phone_number = models.CharField(
        max_length=20, verbose_name=_("Phone Number")
    )
    email = models.EmailField(
        max_length=255, null=True, blank=True,
        verbose_name=_("Email"),
        help_text=_("Optional: Student's email address.")
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='applications',
        verbose_name=_("Course")
    )
    applied_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Applied At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last Updated At")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name=_("Status")
    )
    admin_notes = models.TextField(
        null=True, blank=True, verbose_name=_("Admin Notes")
    )

    def __str__(self):
        return f"Application by {self.full_name} for {
                self.course.get_localized_title('en') if self.course else 'N/A'}"

    class Meta:
        verbose_name = _("Student Application")
        verbose_name_plural = _("Student Applications")
        ordering = ['-applied_at']


# Модель FAQ
class FAQItem(models.Model):
    question_en = models.CharField(
        max_length=500, verbose_name=_("Question (English)")
    )
    answer_en = models.TextField(
        verbose_name=_("Answer (English)")
    )

    question_ru = models.CharField(
        max_length=500, blank=True, null=True,
        verbose_name=_("Question (Russian)")
    )
    answer_ru = models.TextField(
        blank=True, null=True, verbose_name=_("Answer (Russian)")
    )

    question_uz = models.CharField(
        max_length=500, blank=True, null=True,
        verbose_name=_("Question (Uzbek)")
    )
    answer_uz = models.TextField(
        blank=True, null=True, verbose_name=_("Answer (Uzbek)")
    )

    order = models.IntegerField(
        default=0,
        verbose_name=_("Display Order"),
        help_text=_("Items with lower order appear first.")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last Updated At")
    )

    def __str__(self):
        return self.question_en

    class Meta:
        verbose_name = _("FAQ Item")
        verbose_name_plural = _("FAQ Items")
        ordering = ['order', 'question_en']

    def get_localized_question(self, lang_code: str) -> str:
        return getattr(self, f'question_{lang_code}', self.question_en)

    def get_localized_answer(self, lang_code: str) -> str:
        return getattr(self, f'answer_{lang_code}', self.answer_en)


# Модель BotText (для кнопок и сообщений бота)
class BotText(models.Model):
    key = models.CharField(
        max_length=255, unique=True, verbose_name=_("Text Key")
    )
    en = models.TextField(verbose_name=_("English Text"))
    ru = models.TextField(verbose_name=_("Russian Text"))
    uz = models.TextField(verbose_name=_("Uzbek Text"))

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = _("Bot Text")
        verbose_name_plural = _("Bot Texts")
        ordering = ['key']

    def get_localized_text(self, lang_code: str) -> str:
        return getattr(self, lang_code, self.en)


# Модель для новостей
class NewsItem(models.Model):
    title_en = models.CharField(
        max_length=500, verbose_name=_("News Title (English)")
    )
    text_en = models.TextField(verbose_name=_("News Text (English)"))

    title_ru = models.CharField(
        max_length=500, blank=True, null=True,
        verbose_name=_("News Title (Russian)")
    )
    text_ru = models.TextField(
        blank=True, null=True, verbose_name=_("News Text (Russian)")
    )

    title_uz = models.CharField(
        max_length=500, blank=True, null=True,
        verbose_name=_("News Title (Uzbek)")
    )
    text_uz = models.TextField(
        blank=True, null=True, verbose_name=_("News Text (Uzbek)")
    )

    image = models.ImageField(
        upload_to='news_images/',
        null=True, blank=True,
        verbose_name=_("News Image")
    )
    telegram_channel_link = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name=_("Telegram Link"),
        help_text=_("Link to the original post in the Telegram channel.")
    )
    published_date = models.DateTimeField(
        db_index=True, verbose_name=_("Published Date")
    )
    is_active = models.BooleanField(
        default=True, verbose_name=_("Is Active")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last Updated At")
    )

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = _("News Item")
        verbose_name_plural = _("News Items")
        ordering = ['-published_date']

    def get_localized_title(self, lang_code: str) -> str:
        return getattr(self, f'title_{lang_code}', self.title_en)

    def get_localized_text(self, lang_code: str) -> str:
        return getattr(self, f'text_{lang_code}', self.text_en)


# Модель для спикеров открытых уроков
class Speaker(models.Model):
    name_en = models.CharField(
        max_length=255, verbose_name=_("Speaker Name (English)")
        )
    name_ru = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Speaker Name (Russian)")
        )
    name_uz = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Speaker Name (Uzbek)")
        )
    bio_en = models.TextField(
        blank=True, null=True, verbose_name=_("Bio (English)")
        )
    bio_ru = models.TextField(
        blank=True, null=True, verbose_name=_("Bio (Russian)")
        )
    bio_uz = models.TextField(
        blank=True, null=True, verbose_name=_("Bio (Uzbek)")
        )
    photo = models.ImageField(
        upload_to='speaker_photos/',
        null=True, blank=True,
        verbose_name=_("Speaker Photo")
        )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")
        ordering = ['name_en']

    def get_localized_name(self, lang_code: str) -> str:
        return getattr(self, f'name_{lang_code}', self.name_en)

    def get_localized_bio(self, lang_code: str) -> str:
        return getattr(self, f'bio_{lang_code}', self.bio_en)


# Модель для открытых уроков
class OpenLesson(models.Model):
    title_en = models.CharField(
        max_length=255, verbose_name=_("Lesson Title (English)")
        )
    description_en = models.TextField(
        blank=True, null=True, verbose_name=_("Description (English)")
        )
    title_ru = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Lesson Title (Russian)")
        )
    description_ru = models.TextField(
        blank=True, null=True, verbose_name=_("Description (Russian)")
        )
    title_uz = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Lesson Title (Uzbek)")
        )
    description_uz = models.TextField(
        blank=True, null=True, verbose_name=_("Description (Uzbek)")
        )

    lesson_date = models.DateField(verbose_name=_("Lesson Date"))
    start_time = models.TimeField(verbose_name=_("Start Time"))
    end_time = models.TimeField(
        blank=True, null=True, verbose_name=_("End Time")
        )

    speaker = models.ForeignKey(
        Speaker,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='open_lessons',
        verbose_name=_("Speaker")
    )
    online_meeting_url = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name=_("Online Meeting URL"),
        help_text=_("Link to the online meeting (e.g., Zoom, Google Meet).")
    )
    location_or_link = models.CharField(
        max_length=500,
        null=True, blank=True,
        verbose_name=_("Location / Link"),
        help_text=_("Physical location or online meeting link.")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last Updated At")
    )

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = _("Open Lesson")
        verbose_name_plural = _("Open Lessons")
        ordering = ['lesson_date', 'start_time']

    def get_localized_title(self, lang_code: str) -> str:
        return getattr(self, f'title_{lang_code}', self.title_en)

    def get_localized_description(self, lang_code: str) -> str:
        return getattr(self, f'description_{lang_code}', self.description_en)


# Модель для студента (профиль студента)
class Student(models.Model):
    telegram_user = models.OneToOneField(
        TelegramUser,
        on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='student_profile',
        verbose_name=_("Telegram User")
    )
    student_id_number = models.CharField(
        max_length=50, unique=True, db_index=True,
        verbose_name=_("Student ID Number"),
        help_text=_("Unique identifier for the student.")
    )
    full_name = models.CharField(
        max_length=255, verbose_name=_("Full Name")
    )
    date_of_birth = models.DateField(
        null=True, blank=True, verbose_name=_("Date of Birth")
    )
    courses = models.ManyToManyField(
        Course,
        related_name='enrolled_students',
        verbose_name=_("Enrolled Courses")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    enrollment_date = models.DateField(
        auto_now_add=True, verbose_name=_("Enrollment Date")
    )
    enrolled_courses = models.ManyToManyField(
        Course, blank=True,
        related_name='student_course_enrollments',
        verbose_name=_("Enrolled Courses"),
        help_text=_(
            "Courses that the student is currently enrolled in or has completed."
            )
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last Updated At")
    )

    def __str__(self):
        return f"{self.full_name} ({self.student_id_number})"

    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")
        ordering = ['full_name']


# Модель для оценок студентов
class Grade(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='grades',
        verbose_name=_("Student")
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='grades_for_course',
        verbose_name=_("Course")
    )
    lesson_topic_en = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Lesson Topic (English)")
        )
    lesson_topic_ru = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Lesson Topic (Russian)")
        )
    lesson_topic_uz = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Lesson Topic (Uzbek)")
        )
    score = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name=_("Score"),
        validators=[MinValueValidator(0.00)]
    )
    graded_by = models.ForeignKey(
        'TelegramUser', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='given_grades',
        verbose_name=_("Graded By")
        )
    grade_date = models.DateField(verbose_name=_("Grade Date"))
    notes = models.TextField(
        blank=True, null=True,
        verbose_name=_("Notes"),
        help_text=_("Additional notes for this grade.")
    )

    def __str__(self):
        return f"Grade for {self.student.full_name} in {
            self.course.title_en}: {self.score}"

    class Meta:
        verbose_name = _("Grade")
        verbose_name_plural = _("Grades")
        ordering = ['-grade_date', 'student__full_name']

    def get_localized_lesson_topic(self, lang_code: str) -> str:
        return getattr(self, f'lesson_topic_{lang_code}', self.lesson_topic_en)


# Модель для расписания (хранение шаблонов или связи с Google Calendar)
class ScheduleItem(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='schedule',
        verbose_name=_("Course")
    )
    title_en = models.CharField(
        max_length=255, verbose_name=_("Lesson Title (English)")
        )
    title_ru = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Lesson Title (Russian)")
        )
    title_uz = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Lesson Title (Uzbek)")
        )
    # Эти поля могут быть использоваться для шаблона или
    # как метаданные для Google Calendar
    lesson_date = models.DateField(verbose_name=_("Lesson Date"))
    lesson_time = models.CharField(
        max_length=50,
        verbose_name=_("Lesson Time (e.g., 10:00-12:00)"),
        help_text=_("E.g., '10:00-12:00' or 'Monday 14:00'.")
    )
    description_en = models.TextField(
        null=True, blank=True, verbose_name=_("Description (English)")
        )
    description_ru = models.TextField(
        null=True, blank=True, verbose_name=_("Description (Russian)")
        )
    description_uz = models.TextField(
        null=True, blank=True, verbose_name=_("Description (Uzbek)")
        )
    is_active = models.BooleanField(
        default=True, verbose_name=_("Is Active")
        )

    def __str__(self):
        return f"{self.course.get_localized_title('en')} - {self.get_localized_title('en')} ({self.lesson_date})"

    class Meta:
        verbose_name = _("Schedule Item")
        verbose_name_plural = _("Schedule Items")
        ordering = ['lesson_date', 'lesson_time']

    def get_localized_title(self, lang_code: str) -> str:
        return getattr(self, f'title_{lang_code}', self.title_en)

    def get_localized_description(self, lang_code: str) -> str:
        return getattr(self, f'description_{lang_code}', self.description_en)


# Модель для материалов курса (ссылки на внешние ресурсы)
class CourseMaterial(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='materials',
        verbose_name=_("Course")
    )
    title_en = models.CharField(
        max_length=255, verbose_name=_("Material Title (English)")
        )
    description_en = models.TextField(
        null=True, blank=True, verbose_name=_("Description (English)")
        )
    title_ru = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Material Title (Russian)")
        )
    description_ru = models.TextField(
        null=True, blank=True, verbose_name=_("Description (Russian)")
        )
    title_uz = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Material Title (Uzbek)")
        )
    description_uz = models.TextField(
        null=True, blank=True, verbose_name=_("Description (Uzbek)")
        )
    url = models.URLField(
        max_length=500, verbose_name=_("URL"),
        help_text=_("Link to the external material (e.g., Google Drive, Yandex Disk).")
    )
    order = models.IntegerField(default=0, verbose_name=_("Order"))

    def __str__(self):
        return f"{self.course.get_localized_title('en')} - {self.get_localized_title('en')}"

    class Meta:
        verbose_name = _("Course Material")
        verbose_name_plural = _("Course Materials")
        ordering = ['course__title_en', 'title_en']

    def get_localized_title(self, lang_code: str) -> str:
        return getattr(self, f'title_{lang_code}', self.title_en)

    def get_localized_description(self, lang_code: str) -> str:
        return getattr(self, f'description_{lang_code}', self.description_en)


# Модель для краткой истории ("О нас" - "История")
class AboutUsHistory(models.Model):
    title_en = models.CharField(
        max_length=255, verbose_name=_("Title (English)"),
        default=_("Our History")
        )
    title_ru = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Title (Russian)"),
        default=_("Наша История")
        )
    title_uz = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Title (Uzbek)"),
        default=_("Bizning Tarix"))
    content_en = models.TextField(verbose_name=_("Content (English)"))
    content_ru = models.TextField(
        blank=True, null=True, verbose_name=_("Content (Russian)")
        )
    content_uz = models.TextField(
        blank=True, null=True, verbose_name=_("Content (Uzbek)")
        )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last Updated At")
        )

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = _("About Us - History")
        verbose_name_plural = _("About Us - History")


# Модель для преподавательского состава ("О нас" - "Преподаватели")
class TeamMember(models.Model):
    name_en = models.CharField(
        max_length=255, verbose_name=_("Name (English)")
        )
    name_ru = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Name (Russian)")
        )
    name_uz = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Name (Uzbek)")
        )
    position_en = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Position (English)")
        )
    position_ru = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Position (Russian)")
        )
    position_uz = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name=_("Position (Uzbek)")
        )
    bio_en = models.TextField(
        blank=True, null=True, verbose_name=_("Biography (English)")
        )
    bio_ru = models.TextField(
        blank=True, null=True, verbose_name=_("Biography (Russian)")
        )
    bio_uz = models.TextField(
        blank=True, null=True, verbose_name=_("Biography (Uzbek)")
        )
    photo = models.ImageField(
        upload_to='team_photos/',
        null=True, blank=True, verbose_name=_("Photo")
        )
    order = models.IntegerField(default=0, verbose_name=_("Display Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    def __str__(self):
        return self.name_en

    class Meta:
        verbose_name = _("Team Member")
        verbose_name_plural = _("Team Members")
        ordering = ['order', 'name_en']

    def get_localized_name(self, lang_code: str) -> str:
        return getattr(self, f'name_{lang_code}', self.name_en)

    def get_localized_position(self, lang_code: str) -> str:
        return getattr(self, f'position_{lang_code}', self.position_en)

    def get_localized_bio(self, lang_code: str) -> str:
        return getattr(self, f'bio_{lang_code}', self.bio_en)


# Модель для партнеров ("О нас" - "Партнеры")
class Partner(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_("Partner Name")
        )
    logo = models.ImageField(
        upload_to='partner_logos/', null=True, blank=True,
        verbose_name=_("Logo")
        )
    description_en = models.TextField(
        null=True, blank=True, verbose_name=_("Description (English)")
        )
    description_ru = models.TextField(
        null=True, blank=True, verbose_name=_("Description (Russian)")
        )
    description_uz = models.TextField(
        null=True, blank=True, verbose_name=_("Description (Uzbek)")
        )
    website_url = models.URLField(
        max_length=500, blank=True, null=True,
        verbose_name=_("Website URL")
        )
    order = models.IntegerField(default=0, verbose_name=_("Display Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")
        ordering = ['order', 'name']

    def get_localized_description(self, lang_code: str) -> str:
        return getattr(self, f'description_{lang_code}', self.description_en)


# Модель для достижений ("О нас" - "Достижения")
class Achievement(models.Model):
    title_en = models.CharField(
        max_length=255, verbose_name=_("Title (English)")
        )
    description_en = models.TextField(
        null=True, blank=True, verbose_name=_("Description (English)")
        )
    title_ru = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name=_("Title (Russian)")
        )
    description_ru = models.TextField(
        null=True, blank=True, verbose_name=_("Description (Russian)")
        )
    title_uz = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name=_("Title (Uzbek)")
        )
    description_uz = models.TextField(
        null=True, blank=True, verbose_name=_("Description (Uzbek)")
        )
    image = models.ImageField(
        upload_to='achievements/', null=True, blank=True,
        verbose_name=_("Image")
        )
    date = models.DateField(
        blank=True, null=True, verbose_name=_("Date of Achievement")
        )
    order = models.IntegerField(default=0, verbose_name=_("Display Order"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    def __str__(self):
        return self.title_en

    class Meta:
        verbose_name = _("Achievement")
        verbose_name_plural = _("Achievements")
        ordering = ['-date', 'order']

    def get_localized_title(self, lang_code: str) -> str:
        return getattr(self, f'title_{lang_code}', self.title_en)

    def get_localized_description(self, lang_code: str) -> str:
        return getattr(self, f'description_{lang_code}', self.description_en)


# Модель для отзывов ("О нас" - "Отзывы")
class Review(models.Model):
    author_name = models.CharField(
        max_length=255, verbose_name=_("Author Name")
        )
    review_text_en = models.TextField(
        verbose_name=_("Review Text (English)")
        )
    review_text_ru = models.TextField(
        null=True, blank=True, verbose_name=_("Review Text (Russian)")
        )
    review_text_uz = models.TextField(
        null=True, blank=True, verbose_name=_("Review Text (Uzbek)")
        )
    rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], default=5,
        verbose_name=_("Rating (1-5)"),
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_approved = models.BooleanField(
        default=False, verbose_name=_("Is Approved")
        )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At")
        )

    def __str__(self):
        return f"Review by {self.author_name} - {self.rating} stars"

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['-created_at']

    def get_localized_review_text(self, lang_code: str) -> str:
        return getattr(self, f'review_text_{lang_code}', self.review_text_en)


# Модель для контактной информации ("Контакты")
class ContactInfo(models.Model):
    # Используем CharField для полей типа "номер телефона",
    # т.к. они могут содержать символы типа "+" или "()"
    address_en = models.TextField(
        null=True, blank=True, verbose_name=_("Address (English)")
        )
    address_ru = models.TextField(
        null=True, blank=True, verbose_name=_("Address (Russian)")
        )
    address_uz = models.TextField(
        null=True, blank=True, verbose_name=_("Address (Uzbek)")
        )
    phone_number = models.CharField(
        max_length=50, null=True, blank=True,
        verbose_name=_("Phone Number")
        )
    email = models.EmailField(
        max_length=255, null=True, blank=True,
        verbose_name=_("Email Address")
        )
    website_url = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name=_("Website URL")
        )
    map_url = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name=_("Map URL"),
        help_text=_("Link to Google Maps or other map service.")
        )
    telegram_channel_url = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name=_("Telegram Channel URL")
        )
    instagram_url = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name=_("Instagram URL")
        )
    facebook_url = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name=_("Facebook URL")
        )
    youtube_url = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name=_("YouTube URL")
        )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Last Updated At")
        )

    def __str__(self):
        return _("Contact Information Settings")

    class Meta:
        verbose_name = _("Contact Information")
        verbose_name_plural = _("Contact Information")

    def get_localized_address(self, lang_code: str) -> str:
        return getattr(self, f'address_{lang_code}', self.address_en)
