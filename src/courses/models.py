from django.db import models
import helpers
from cloudinary.models import CloudinaryField
import uuid
from django.urls import reverse
from django.utils.text import slugify


helpers.cloudinary_init()
class PublishStatus(models.TextChoices):
        PUBLISHED = ('published', 'Published')
        COMING_SOON = ('coming soon', 'Coming Soon')
        DRAFT = ('draft', 'Draft')


class AccessRequirements(models.TextChoices):
     ANYONE = ('anyone', 'Anyone')
     EMAIL_REQUIRED = ('email required', 'Email Required')
     

def handle_upload(instance, filename):
     return f'{filename}'

def get_public_id(instance, *args, **kwargs):
     unique_id = str(uuid.uuid4()).replace('-', '')
     title = instance.title
     if not title:
          return unique_id
     short_unique_id = unique_id[:5]
     slug = slugify(title)
     return f'{slug}-{short_unique_id}'

def get_public_id_prefix(instance, *args, **kwargs):
     public_id = instance.public_id
     return f'courses/{public_id}'

def get_display_name(instance, *args, **kwargs):
     if hasattr(instance, 'path'):
          path = instance.path
          if path.startswith('/'):
               path = path[1:]
          if path.endswith('/'):
               path = path[:-1]
          return path
     if hasattr(instance, get_display_name):
          return instance.get_display_name()
     elif hasattr(instance, 'title'):
          return instance.title
     model_class = instance.__class__
     model_name = model_class.__name__
     public_id = instance.public_id
     model_name_slug = slugify(model_name)
     if not public_id:
          return f'{model_name_slug}'
     return f'{model_name_slug}-{public_id}'

class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    access = models.CharField(max_length=20, choices=AccessRequirements.choices, default=AccessRequirements.EMAIL_REQUIRED)
#   image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    public_id = models.CharField(max_length=130, blank=True, null=True)
    image = CloudinaryField(
         'image', 
          null=True, 
          public_id_prefix=get_public_id_prefix, 
          display_name=get_display_name,
          tags = ['course', 'thumbnail']
     )
    status = models.CharField(max_length=20, choices=PublishStatus.choices, default=PublishStatus.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated  = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
         
         if self.public_id == '' or self.public_id is None:
              self.public_id = get_public_id(self)

         super().save(*args, **kwargs)
     
    def get_display_name(self):
         return f'{self.title}-Course'

    
    def get_absolute_url(self):
         return self.path
    
    def course_detail_url(self):
         return reverse('courses:list_detail', kwargs={'course_id':self.id})

    @property
    def path(self):
         return f'/courses-{self.public_id}'

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    

class Lesson(models.Model):
     title = models.CharField(max_length=120)
     description = models.TextField(blank=True, null=True)
     public_id = models.CharField(max_length=130, blank=True, null=True, db_index=True)
     course = models.ForeignKey(Course, on_delete=models.CASCADE)
     thumbnail = CloudinaryField(
         'image', 
          blank=True, 
          null=True,
          public_id_prefix=get_public_id_prefix, 
          display_name=get_display_name,
          tags = ['image', 'thumbnail', 'lesson']
     )
     video = CloudinaryField(
          'video', 
          blank=True, 
          null=True, 
          resource_type='video',
          public_id_prefix=get_public_id_prefix,
          display_name=get_display_name,
          tags = ['video', 'lesson']
          )
     status = models.CharField(max_length=20, choices=PublishStatus.choices, default=PublishStatus.PUBLISHED)
     can_preview = models.BooleanField(default=False, help_text='if user does not have access to course, can they see this?')
     order = models.IntegerField(default=0)
     timestamp = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)
     class Meta:
          ordering = ['order', '-updated']


     def save(self, *args, **kwargs):
          if self.public_id == '' or self.public_id is None:
              self.public_id = get_public_id(self)
          super().save(*args, **kwargs)


     def get_absolute_url(self):
          return self.path

     @property
     def path(self):
          course_path = self.course.path
          if course_path.endswith('/'):
               course_path = course_path[:-1]
          return f'{course_path}-lessons-{self.public_id}'
     
     def get_display_name(self):
          return f'{self.title}-{self.course.get_display_name()}'
     
     @property
     def requires_email(self):
          return self.course.access == AccessRequirements.EMAIL_REQUIRED

     @property
     def is_coming_soon(self):
          return self.status == PublishStatus.COMING_SOON
     
     @property
     def has_video(self):
          return self.video is not None 