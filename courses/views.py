from django.shortcuts import render
from courses.models import Course, Category
from django.db.models import Avg, Count

def landing_page(request):
    courses = (
        Course.objects.filter(is_published=True)
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
