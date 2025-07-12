from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.contrib import messages
from django.urls import reverse
from courses.models import Course
from courses.forms import CourseForm

def instructor_required(view_func):
    """Decorator to ensure user is an instructor"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_instructor:
            messages.error(request, "You must be an instructor to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@instructor_required
def instructor_dashboard(request):
    """Instructor dashboard view"""
    courses = Course.objects.filter(instructor=request.user)
    
    context = {
        'courses_count': courses.count(),
        'total_enrollments': sum(c.enrollments.count() for c in courses),
        'recent_courses': courses.order_by("-created_at")[:5],
    }
    
    return render(request, 'instructor/dashboard.html', context)

@login_required
@instructor_required
def my_courses(request):
    """List instructor's courses with pagination"""
    courses = (
        Course.objects.filter(instructor=request.user)
        .select_related("category")
        .prefetch_related("likes", "reviews")
        .annotate(
            avg_rating=Avg("reviews__rating"),
            likes_count=Count("likes")
        )
        .order_by("-created_at")
    )
    
    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'courses': page_obj,
        'page_obj': page_obj,
    }
    
    return render(request, 'instructor/my_courses.html', context)

@login_required
@instructor_required
def course_create(request):
    """Create a new course"""
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('instructor:my_courses')
    else:
        form = CourseForm()
    
    context = {
        'form': form,
        'title': 'Create Course',
    }
    
    return render(request, 'instructor/course_form.html', context)

@login_required
@instructor_required
def course_update(request, pk):
    """Update an existing course"""
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('instructor:my_courses')
    else:
        form = CourseForm(instance=course)
    
    context = {
        'form': form,
        'course': course,
        'title': 'Update Course',
    }
    
    return render(request, 'instructor/course_form.html', context)

@login_required
@instructor_required
def course_delete(request, pk):
    """Delete a course"""
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('instructor:my_courses')
    
    context = {
        'course': course,
    }
    
    return render(request, 'instructor/course_confirm_delete.html', context)