from django.contrib import admin
from .models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'content', 'timestamp')
    list_filter = ('course',)
    search_fields = ('student__username', 'content')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'question', 'timestamp')
    search_fields = ('instructor__username', 'question__content')
