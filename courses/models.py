from django.db import models
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='courses')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor_courses')
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True)
    
    is_published = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_courses', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def total_lessons(self):
        return self.lessons.count()

    def progress_for_user(self, user):
        if not user.is_authenticated:
            return 0
        completed = self.courseprogress_set.filter(student=user, completed=True).count()
        total = self.lessons.count()
        if total == 0:
            return 0
        return int((completed / total) * 100)
    
    def get_next_lesson(self, user):
        completed_ids = self.courseprogress_set.filter(student=user, completed=True).values_list('lesson_id', flat=True)
        return self.lessons.exclude(id__in=completed_ids).order_by('order').first()

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def average_rating(self):
        avg = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        return round(avg or 0, 1)

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        default=5
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'user')  # 1 review per user per course

    def __str__(self):
        return f"{self.user.username} - {self.course.title} ({self.rating})"

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Like(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'course')

class Follow(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ('student', 'instructor')
