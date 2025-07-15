from django.urls import path, include
from .views import course_detail, course_dashboard, mark_lesson_complete
from interactions.views import qna_view

app_name = 'courses'

urlpatterns = [
    path('<int:pk>/', course_detail, name='course_detail'),
    path('<int:pk>/dashboard/', course_dashboard, name='course_dashboard'),
    path('<int:pk>/dashboard/complete/', mark_lesson_complete, name='mark_lesson_complete'),
    path('<int:course_id>/dashboard/', include('interactions.urls', namespace='interactions')),
]
