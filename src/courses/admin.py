from django.contrib import admin
from .models import Course, Lesson
from helpers._cloudinary.services import get_display_image, get_display_video
class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    readonly_fields = ['updated', 'display_image', 'display_video']
    extra = 0

    display_image = get_display_image
    display_video = get_display_video
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'access']
    list_filter = ['status', 'access']
    fields = ['public_id', 'title', 'description', 'status', 'timestamp', 'updated', 'image', 'access', 'display_image']
    readonly_fields = ['display_image', 'timestamp', 'updated', 'public_id']
    inlines = [LessonInlineAdmin]

    display_image = get_display_image

    display_image.short_description = 'Image'