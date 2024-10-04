import cloudinary
from django.conf import settings

CLOUD_NAME = settings.CLOUD_NAME
PUBLIC_API_KEY = settings.PUBLIC_API_KEY
SECRET_API_KEY = settings.SECRET_API_KEY
def cloudinary_init():
    cloudinary.config( 
        cloud_name = CLOUD_NAME, 
        api_key = PUBLIC_API_KEY, 
        api_secret = SECRET_API_KEY,
        secure=True
    )
