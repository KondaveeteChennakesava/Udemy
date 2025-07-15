from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from courses.models import Course, Category, Lesson, Review
from accounts.models import User
from django.db.models import Avg, Count, Prefetch
from enrollments.models import Enrollment, CourseProgress
from interactions.models import Question, Answer

def course_list(request):
    category_slug = request.GET.get("category")

    base_queryset = Course.objects.filter(is_published=True)

    if category_slug:
        base_queryset = base_queryset.filter(category__slug=category_slug)

    courses = (
        base_queryset
        .select_related('instructor', 'category')
        .prefetch_related(
            'likes',
            'reviews',
            Prefetch('enrollments', queryset=Enrollment.objects.only('id', 'course_id'))
        )
        .annotate(
            avg_rating=Avg('reviews__rating'),
            likes_count=Count('likes', distinct=True),
            total_enrollments=Count('enrollments', distinct=True),
            reviews_count=Count('reviews', distinct=True)
        )
        .order_by('-created_at')
    )

    categories = Category.objects.all().order_by('name')

    return courses, categories


def landing_page(request):
    courses, categories = course_list(request)

    total_courses = Course.objects.filter(is_published=True).count()
    total_instructors = User.objects.filter(is_instructor=True).count()
    total_students = User.objects.filter(is_instructor=False).count()
    total_reviews = Review.objects.count()

    return render(request, 'landing.html', {
        'courses': courses,
        'categories': categories,
        'total_courses': total_courses,
        'total_instructors': total_instructors,
        'total_students': total_students,
        'total_reviews': total_reviews,
    })

def course_detail(request, pk):
    course = get_object_or_404(
        Course.objects.select_related('instructor', 'category')
        .prefetch_related(
            Prefetch('lessons', queryset=Lesson.objects.order_by('order')),
            Prefetch('reviews', queryset=Review.objects.select_related('user').order_by('-created_at')),
            'likes'
        )
        .annotate(
            avg_rating=Avg('reviews__rating'),
            likes_count=Count('likes', distinct=True),
            total_enrollments=Count('enrollments', distinct=True),
            reviews_count=Count('reviews', distinct=True)
        ),
        pk=pk
    )

    lessons = course.lessons.all()
    reviews = course.reviews.all()

    enrolled = False
    if request.user.is_authenticated and not request.user.is_instructor:
        enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    if request.method == 'POST' and request.user.is_authenticated and not request.user.is_instructor:
        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course
        )
        if created:
            enrolled = True
        return redirect('courses:course_detail', pk=course.pk)

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'reviews': reviews,
        'enrolled': enrolled,
    })


@login_required
def course_dashboard(request, pk):
    course = get_object_or_404(
        Course.objects.select_related('instructor', 'category')
        .prefetch_related(
            Prefetch('lessons', queryset=Lesson.objects.order_by('order')),
            'reviews'
        ),
        pk=pk
    )
    
    enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
    
    lessons = course.lessons.all().order_by('order')
    
    completed_lesson_ids = CourseProgress.objects.filter(
        student=request.user,
        course=course,
        completed=True
    ).values_list('lesson_id', flat=True)

    
    for lesson in lessons:
        lesson.is_completed = lesson.id in completed_lesson_ids
    
    total_lessons = lessons.count()
    completed_lessons = len(completed_lesson_ids)
    progress = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    remaining_lessons = total_lessons - completed_lessons
    
    next_lesson = None
    for lesson in lessons:
        if not lesson.is_completed:
            next_lesson = lesson
            break
    
    circumference = 2 * 3.14159 * 52
    progress_offset = circumference - (progress / 100) * circumference


    questions = Question.objects.filter(course=course).select_related('student').prefetch_related('answers__user').order_by('-created_at')
    total_answers = Answer.objects.filter(question__course=course).count()
    context = {
        'course': course,
        'lessons': lessons,
        'enrollment': enrollment,
        'progress': round(progress),
        'progress_offset': progress_offset,
        'completed_lessons': completed_lessons,
        'total_lessons': total_lessons,
        'remaining_lessons': remaining_lessons,
        'next_lesson': next_lesson,
        'questions': questions,
        'total_answers': total_answers,
    }
    
    return render(request, 'courses/course_dashboard.html', context)

@login_required
@require_POST
def mark_lesson_complete(request, pk):
    try:
        course = get_object_or_404(Course, pk=pk)
        lesson_id = request.POST.get('lesson_id')
        
        print(f"Course ID received: {pk}")
        print(f"Request: {request}")
        print(f"POST data: {request.POST.get('lesson_id')}")
        print(f"POST data (dict): {request.POST.dict()}")
        print(f"Lesson ID received: {lesson_id}")
        
        if not lesson_id or not lesson_id.isdigit():
            return JsonResponse({
                'success': False,
                'error': 'Invalid or missing lesson ID',
                'post_data': request.POST.dict()
            })

        
        try:
            lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Lesson not found: {str(e)}',
                'lesson_id': lesson_id,
                'course_id': pk
            })
        
        try:
            enrollment = get_object_or_404(Enrollment, student=request.user, course=course)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Enrollment not found: {str(e)}'
            })
        
        progress, created = CourseProgress.objects.get_or_create(
            student=request.user,
            course=course,
            lesson=lesson,
            defaults={'completed': True}
        )
        
        if not created and not progress.completed:
            progress.completed = True
            progress.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Lesson marked as complete',
            'lesson_id': lesson.id,
            'created': created
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        })