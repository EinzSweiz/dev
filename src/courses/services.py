from .models import Course, AccessRequirements, PublishStatus, Lesson


def get_publish_courses():
    return Course.objects.filter(status=PublishStatus.PUBLISHED)

#NOTE Can be added
# def get_course_details(course_id=None):
#     if course_id is None:
#         return None
#     obj = None
#     try:
#         obj = Course.objects.get(
#             status=PublishStatus.PUBLISHED,
#             id=course_id
#         ) 
#     except Exception:
#         return f'{Exception}'
#     return obj


# def get_lesson_details(course_id=None, lesson_id=None):
#     if course_id is None and lesson_id is None:
#         return None
    
#     obj = None
#     try:
#         obj = Lesson.objects.get(
#             course__id = course_id,
#             course__status = PublishStatus.PUBLISHED,
#             status = PublishStatus.PUBLISHED,
#             id = lesson_id
#         )
#     except Exception:
#         return f'{Exception}'
#     return obj