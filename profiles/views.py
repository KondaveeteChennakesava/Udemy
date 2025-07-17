import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from accounts.models import User, Profile
from courses.models import Course
from enrollments.models import Enrollment
from .forms import EditProfileForm, EditUserForm

@login_required
def edit_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    if request.user != profile.user:
        raise PermissionDenied

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            cropped_data = request.POST.get('cropped_image')
            if cropped_data:
                try:
                    format, imgstr = cropped_data.split(';base64,')
                    ext = format.split('/')[-1]
                    file_name = f"{request.user.username}_profile.{ext}"
                    profile.profile_picture = ContentFile(base64.b64decode(imgstr), name=file_name)
                    profile.save()
                except Exception as e:
                    print("Failed to save cropped image:", e)

            return redirect('profiles:profile', username=request.user.username)
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=profile)

    return render(request, 'profiles/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile

    is_following = False
    if request.user.is_authenticated and user_obj != request.user and user_obj.is_instructor:
        is_following = profile.followers.filter(id=request.user.id).exists()

    if user_obj.is_instructor:
        courses = Course.objects.filter(instructor=user_obj)
    else:
        enrollments = Enrollment.objects.filter(student=user_obj).select_related('course')
        courses = [enrollment.course for enrollment in enrollments]

    return render(request, 'profiles/profile.html', {
        'user_obj': user_obj,
        'profile': profile,
        'is_following': is_following,
        'courses': courses,
    })



@login_required
def toggle_follow(request, username):
    instructor = get_object_or_404(User, username=username, is_instructor=True)
    profile = instructor.profile

    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)

    return redirect('profiles:profile', username=username)
