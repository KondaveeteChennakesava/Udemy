from django.contrib import admin
from .models import Enrollment, CourseProgress

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course',)
    search_fields = ('student__username', 'course__title')

@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'lesson', 'completed', 'last_updated')
    list_filter = ('course', 'completed')
    search_fields = ('student__username', 'lesson__title')
