from django.contrib import admin
from .models import Category, Course, Lesson, Like, Follow, Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'course__title')

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'category', 'likes_count_display', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    inlines = [LessonInline]

    def likes_count_display(self, obj):
        return obj.likes.count()
    
    likes_count_display.short_description = 'Likes'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('student', 'instructor')
