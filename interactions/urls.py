from django.urls import path
from . import views

app_name = 'interactions'

urlpatterns = [
    path('', views.qna_view, name='course_qna'),
    path('qna/post-question/', views.post_question, name='post_question'),
    path('qna/<int:question_id>/post-answer/', views.post_answer, name='post_answer'),
]