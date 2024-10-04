from django.utils.html import format_html
from django.template.loader import get_template
from django.conf import settings

def get_cloudinary_object(instance, field_name='image'):
    image_options = {
        'width': 200
    }
    
    if instance.image:
        cloudinary_html = instance.image.image(**image_options)
    else:
        return ""

    return cloudinary_html

def get_image_thumbnail(instance, width=500):
          image_options = {
               'width': width
          }
          return instance.thumbnail.image(**image_options)

def get_video_thumbnail(
        instance, 
        width=None, 
        height=None, 
        sign_url=False, 
        fetch_format='auto', 
        quality='auto', 
        field_name='video',
        autoplay=True,
        controls=True,):
    

    video_options = {
        'sign_url': sign_url,
        'fetch_format': fetch_format,
        'quality': quality,
        'controls': controls,
        'autoplay': autoplay,
    }
    
    if width is not None:
        video_options['width'] = width
    if height is not None:
        video_options['height'] = height
    
    if width is not None and height is not None:
        video_options['crop'] = 'limit'
    
    if hasattr(instance, field_name) and getattr(instance, field_name):
        return getattr(instance, field_name).build_url(**video_options)
    else:
        return ""

def get_display_image(self, obj, *args, **kwargs):
    if obj.__class__.__name__ == 'Course':
        cloudinary_html = get_cloudinary_object(obj)
    else:
        cloudinary_html = get_image_thumbnail(obj, width=200)
    return format_html(cloudinary_html)

def get_display_video(self, obj, *args, **kwargs):
    cloudinary_html = get_video_thumbnail(obj, field_name='video', width=350, height=350)
    print(cloudinary_html)
    template_name = "videos/snippets/embed.html"
    tmpl = get_template(template_name)
    cloud_name = settings.CLOUD_NAME
    _html = tmpl.render({'video_url': cloudinary_html, 'cloud_name':cloud_name})
    return _html