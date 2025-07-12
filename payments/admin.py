from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount', 'payment_id', 'status', 'paid_at')
    list_filter = ('status',)
    search_fields = ('student__username', 'payment_id', 'course__title')
