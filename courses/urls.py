from django.urls import path, include
from .views import course_detail, course_dashboard, mark_lesson_complete, toggle_like, add_review, update_review, delete_review
from interactions.views import qna_view

app_name = 'courses'

urlpatterns = [
    path('<int:pk>/', course_detail, name='course_detail'),
    path('<int:course_id>/like/', toggle_like, name='toggle_like'),
    path('<int:course_id>/review/add/', add_review, name='add_review'),
    path('<int:course_id>/review/update/', update_review, name='update_review'),
    path('<int:course_id>/review/delete/', delete_review, name='delete_review'),
    path('<int:pk>/dashboard/', course_dashboard, name='course_dashboard'),
    path('<int:pk>/dashboard/complete/', mark_lesson_complete, name='mark_lesson_complete'),
    path('<int:course_id>/dashboard/', include('interactions.urls', namespace='interactions')),
]
