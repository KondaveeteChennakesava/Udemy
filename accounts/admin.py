from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_instructor', 'is_staff', 'is_active')
    list_filter = ('is_instructor', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    ordering = ('id',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture')
