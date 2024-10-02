import cloudinary
from decouple import config


CLOUD_NAME = config('CLOUD_NAME', default="")
PUBLIC_API_KEY = config('PUBLIC_API_KEY', default="")
SECRET_API_KEY = config('SECRET_API_KEY')
def cloudinary_init():
    cloudinary.config( 
        cloud_name = CLOUD_NAME, 
        api_key = PUBLIC_API_KEY, 
        api_secret = SECRET_API_KEY,
        secure=True
    )
