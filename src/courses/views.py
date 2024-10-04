from typing import Any
from helpers._cloudinary.services import get_display_video
from django.db.models.base import Model as Model
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Course, Lesson
from .models import PublishStatus
from django.db.models import Exists, OuterRef
from . import services

class CourseList(ListView):
   model = Course
   template_name = 'courses/course_list.html'
   context_object_name = 'courses'
   ordering = ['-updated'] 

   def get_queryset(self, *args, **kwargs):
       published_lessons = Lesson.objects.filter(course=OuterRef('pk'), status=PublishStatus.PUBLISHED)
       qs =  services.get_publish_courses()
       return qs.annotate(has_published_lessons=Exists(published_lessons)).filter(has_published_lessons=True)
       
#    def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         courses_with_videos = []

#         for course in context['courses']:
#             # Get the first published lesson for each course
#             first_lesson_with_video = course.lesson_set.filter(status=PublishStatus.PUBLISHED).first()
#             video = get_display_video(self, first_lesson_with_video) if first_lesson_with_video else None
#             courses_with_videos.append({
#                 'video': video
#             })

#         context['courses_with_videos'] = courses_with_videos
#         return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        course_id = self.kwargs.get('course_id')
        return get_object_or_404(Course, id=course_id, status=PublishStatus.PUBLISHED)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = self.object.lesson_set.filter(status=PublishStatus.PUBLISHED)
        return context
    
class LessonDetail(DetailView):
    model = Lesson
    template_name = 'lesson/lesson_detail.html'
    context_object_name = 'lesson'
    ordering = ['-updated']


    def get_object(self, queryset=None):
        course_id = self.kwargs.get('course_id')
        lesson_id = self.kwargs.get('lesson_id')
        return get_object_or_404(Lesson, course_id=course_id, id=lesson_id, status=PublishStatus.PUBLISHED)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video_html = get_display_video(self=self, obj=self.object)
        if self.object.has_video:
            context['video_embed'] = video_html
        return context
