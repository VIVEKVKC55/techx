from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone


class Subscription(models.Model):
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium-A'),
        ('scalable', 'Premium-B'),
    ]
    
    DURATION_CHOICES = [
        (30, "1 Month"),
        (90, "3 Months"),
        (365, "1 Year"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='basic')
    duration_days = models.IntegerField(choices=DURATION_CHOICES, blank=True, null=True)  # Only for premium/scalable
    extra_slots = models.PositiveIntegerField(default=0)  # Purchased slots
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField(blank=True, null=True)  # Nullable for Basic plan
    is_approved = models.BooleanField(default=False)  # NEW: Approval status
    pending_plan = models.CharField(max_length=10, blank=True, null=True)  # NEW: Requested plan
    pending_duration = models.IntegerField(blank=True, null=True)  # NEW: Requested duration

    def save(self, *args, **kwargs):
        """Only apply changes if the subscription is approved."""
        if self.is_approved and self.pending_plan:
            self.plan = self.pending_plan
            self.duration_days = self.pending_duration
            self.start_date = now()
            self.end_date = now() + timedelta(days=self.duration_days or 30)  # Default to 1 month
            self.pending_plan = None  # Clear pending request
            self.pending_duration = None
        super().save(*args, **kwargs)

    def is_active(self):
        """Check if the subscription is still valid and approved."""
        if self.plan == 'basic' or self.end_date is None:
            return True  # Basic users are always active
        return self.end_date >= now() and self.is_approved  # Only active if approved

    def remaining_days(self):
        """Calculate remaining days if end_date exists."""
        if self.end_date:
            now_time = now()
            delta = (self.end_date - now_time).days
            return max(delta, 0)  # Avoid negative values
        return "Unlimited"

    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()} ({self.get_duration_days_display() if self.duration_days else 'Free'})"


class ProductView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viewed_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="user_views")
    viewed_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ("user", "product")  # Prevent duplicate views per user per product

    def __str__(self):
        return f"{self.user.username} viewed {self.product.name}"
