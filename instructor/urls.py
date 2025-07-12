from django.urls import path
from . import views

app_name = 'instructor'

urlpatterns = [
    path('', views.instructor_dashboard, name='instructor_dashboard'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('course/create/', views.course_create, name='course_create'),
    path('course/<int:pk>/update/', views.course_update, name='course_update'),
    path('course/<int:pk>/delete/', views.course_delete, name='course_delete'),
]