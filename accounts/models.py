from django.contrib.auth.models import AbstractUser
from django.db import models

def user_profile_upload_path(instance, filename):
    return f'profiles/user_{instance.user.id}/{filename}'

class User(AbstractUser):
    is_instructor = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to=user_profile_upload_path, blank=True, null=True)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField('User', related_name='following_instructors', blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    social_github = models.URLField(blank=True, null=True)
    social_linkedin = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def total_followers(self):
        return self.followers.count()
