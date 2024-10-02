from django.contrib import admin
from .models import Course, Lesson
from django.utils.html import format_html
from cloudinary import CloudinaryImage

class LessonInlineAdmin(admin.StackedInline):
    model = Lesson
    readonly_fields = ['updated']
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'access']
    list_filter = ['status', 'access']
    fields = ['public_id', 'title', 'description', 'status', 'timestamp', 'updated', 'image', 'access', 'display_image']
    readonly_fields = ['display_image', 'timestamp', 'updated', 'public_id']
    inlines = [LessonInlineAdmin]


    def display_image(self, obj, *args, **kwargs):
        cloudinary_html = obj.image_admin
        return  format_html(cloudinary_html)
    
    display_image.short_description = 'Image'