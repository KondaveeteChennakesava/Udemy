from django.shortcuts import redirect, get_object_or_404
from courses.models import Course
from .models import Enrollment
from django.contrib.auth.decorators import login_required

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    Enrollment.objects.get_or_create(student=request.user, course=course)
    return redirect('courses:course_dashboard', pk=course_id)
