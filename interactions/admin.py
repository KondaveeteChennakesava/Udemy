from django.contrib import admin
from .models import Question, Answer

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'content_preview', 'created_at', 'is_resolved')
    list_filter = ('course', 'is_resolved', 'created_at')
    search_fields = ('student__username', 'content')
    readonly_fields = ('created_at', 'updated_at')
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content"

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_preview', 'content_preview', 'created_at', 'is_best_answer', 'parent')
    list_filter = ('is_best_answer', 'created_at')
    search_fields = ('user__username', 'content', 'question__content')
    readonly_fields = ('created_at', 'updated_at')
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Content"
    
    def question_preview(self, obj):
        return obj.question.content[:30] + "..." if len(obj.question.content) > 30 else obj.question.content
    question_preview.short_description = "Question"