from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('<str:username>/', views.profile_view, name='profile'),
    path('<str:username>/follow/', views.toggle_follow, name='toggle_follow'),
    path('<str:username>/edit/', views.edit_profile, name='edit_profile'),
]
