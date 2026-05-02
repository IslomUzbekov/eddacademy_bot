from bot.application.dto.registration import CourseApplicationInput
from bot.services.application_service import application_service
from bot.services.course_service import course_service
from bot.services.user_service import user_service


class SubmitCourseApplicationUseCase:
    async def execute(self, data: CourseApplicationInput):
        course = await course_service.get_course_by_id(data.course_id) if data.course_id else None
        if course is None:
            active_courses = await course_service.get_active_courses()
            if not active_courses:
                return None
            course = active_courses[0]

        telegram_user = await user_service.get_user_by_id(data.telegram_user_id)
        if telegram_user is None:
            return None

        await application_service.create_application(
            telegram_user=telegram_user,
            full_name=data.full_name,
            phone_number=data.phone_number,
            course=course,
            student_full_name=data.student_full_name,
            student_age=data.student_age,
            is_self_application=data.is_self_application,
        )
        return course

submit_course_application_use_case = SubmitCourseApplicationUseCase()
