from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('list/', views.CourseList.as_view(), name='list'),
    path('list/<int:course_id>/', views.CourseDetailView.as_view(), name='list_detail'),
    path('list/<int:course_id>/lessons/<int:lesson_id>/', views.LessonDetail.as_view(), name='lesson_detail'),

]