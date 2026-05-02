from dataclasses import dataclass


@dataclass(frozen=True)
class CourseApplicationInput:
    telegram_user_id: int
    full_name: str
    phone_number: str
    student_full_name: str
    student_age: int
    if_self_application: bool
    course_id: int | None = None
