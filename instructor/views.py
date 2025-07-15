from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from courses.models import Course
from courses.forms import CourseForm

def instructor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_instructor:
            messages.error(request, "You must be an instructor to access this page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@instructor_required
def instructor_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    
    total_courses = courses.count()
    published_courses = courses.filter(is_published=True).count()
    total_enrollments = sum(c.enrollments.count() for c in courses)
    total_likes = sum(c.likes.count() for c in courses)
    
    avg_rating = courses.aggregate(
        avg_rating=Avg('reviews__rating')
    )['avg_rating'] or 0
    
    context = {
        'courses_count': total_courses,
        'published_courses': published_courses,
        'total_enrollments': total_enrollments,
        'total_likes': total_likes,
        'avg_rating': round(avg_rating, 1),
        'recent_courses': courses.order_by("-created_at")[:5],
    }
    
    return render(request, 'instructor/dashboard.html', context)

@login_required
@instructor_required
def my_courses(request):
    courses = Course.objects.filter(instructor=request.user)
    
    search_query = request.GET.get('search', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    status_filter = request.GET.get('status', '')
    if status_filter == 'published':
        courses = courses.filter(is_published=True)
    elif status_filter == 'draft':
        courses = courses.filter(is_published=False)
    
    category_filter = request.GET.get('category', '')
    if category_filter:
        courses = courses.filter(category__slug=category_filter)
    
    courses = (
        courses
        .select_related("category")
        .prefetch_related("likes", "reviews", "enrollments")
        .annotate(
            avg_rating=Avg("reviews__rating"),
            likes_count=Count("likes"),
            enrollments_count=Count("enrollments")
        )
        .order_by("-created_at")
    )
    
    paginator = Paginator(courses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    from courses.models import Category
    categories = Category.objects.all()
    
    context = {
        'courses': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'categories': categories,
    }
    
    return render(request, 'instructor/my_courses.html', context)

@login_required
@instructor_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                course = form.save(commit=False)
                course.instructor = request.user
                course.save()
                messages.success(request, f'Course "{course.title}" created successfully!')
                
                if 'save_and_continue' in request.POST:
                    return redirect('instructor:course_update', pk=course.pk)
                else:
                    return redirect('instructor:my_courses')
            except Exception as e:
                messages.error(request, f'Error creating course: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm()
    
    context = {
        'form': form,
        'title': 'Create New Course',
        'action': 'create',
    }
    
    return render(request, 'instructor/course_form.html', context)

@login_required
@instructor_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            try:
                updated_course = form.save()
                messages.success(request, f'Course "{updated_course.title}" updated successfully!')
                
                if 'save_and_continue' in request.POST:
                    return redirect('instructor:course_update', pk=course.pk)
                else:
                    return redirect('instructor:my_courses')
            except Exception as e:
                messages.error(request, f'Error updating course: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseForm(instance=course)
    
    context = {
        'form': form,
        'course': course,
        'title': f'Update "{course.title}"',
        'action': 'update',
    }
    
    return render(request, 'instructor/course_form.html', context)

@login_required
@instructor_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    
    if request.method == 'POST':
        course_title = course.title
        try:
            course.delete()
            messages.success(request, f'Course "{course_title}" has been deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting course: {str(e)}')
        
        return redirect('instructor:my_courses')
    
    enrollments_count = course.enrollments.count()
    reviews_count = course.reviews.count()
    likes_count = course.likes.count()
    
    context = {
        'course': course,
        'enrollments_count': enrollments_count,
        'reviews_count': reviews_count,
        'likes_count': likes_count,
    }
    
    return render(request, 'instructor/course_confirm_delete.html', context)
