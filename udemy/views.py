from django.shortcuts import render
from courses.models import Course, Category
from django.db.models import Avg, Count

def landing(request):
    category_slug = request.GET.get('category')

    courses = Course.objects.filter(is_published=True)

    if category_slug:
        courses = courses.filter(category__slug=category_slug)

    courses = (
        courses
        .select_related('category', 'instructor')
        .prefetch_related('reviews', 'likes')
        .annotate(
            avg_rating=Avg('reviews__rating'),
            likes_count=Count('likes')
        )
        .order_by('-created_at')
    )

    categories = Category.objects.all()

    return render(request, 'landing.html', {
        'courses': courses,
        'categories': categories,
    })
