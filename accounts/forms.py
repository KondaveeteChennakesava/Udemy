from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_instructor = forms.BooleanField(required=False, label='Register as Instructor')

    class Meta:
        model = User
        fields = ('username', 'email', 'is_instructor', 'password1', 'password2')
