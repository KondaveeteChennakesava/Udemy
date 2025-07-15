from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Question, Answer
from courses.models import Course
from enrollments.models import Enrollment

@login_required
def qna_view(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        return HttpResponseForbidden("You must be enrolled to view Q&A")

    questions = Question.objects.filter(course=course).select_related('student').prefetch_related('answers__replies', 'answers__instructor')

    return JsonResponse({
        'course': course,
        'questions': questions,
    })


@login_required
def post_question(request, course_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        course = get_object_or_404(Course, pk=course_id)

        if not Enrollment.objects.filter(student=request.user, course=course).exists():
            return HttpResponseForbidden("Only enrolled students can ask questions.")

        Question.objects.create(student=request.user, course=course, content=content)
    return redirect('courses:course_dashboard', pk=course_id)


@login_required
def post_answer(request, course_id, question_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')

        question = get_object_or_404(Question, pk=question_id)

        parent = Answer.objects.filter(pk=parent_id).first() if parent_id else None

        Answer.objects.create(
            user=request.user,
            question=question,
            content=content,
            parent=parent
        )

        return redirect('courses:course_dashboard', pk=course_id)
