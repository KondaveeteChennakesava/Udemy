from django.db import models
from accounts.models import User
from courses.models import Course

class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} paid {self.amount} for {self.course.title}"
