from django.urls import path
from . import views

app_name = 'email'

urlpatterns =  [
    path('verify/<uuid:token>/', views.verify_email_token_view, name='verify_email'),
    path('hx/login/', views.email_token_login_view , name='login'),
    path('hx/logout/', views.logout_btn_hx_view, name='logout'),

]