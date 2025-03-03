from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
from django.utils.timezone import now
from datetime import timedelta

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

    def save(self, *args, **kwargs):
        """Set end date only for premium/scalable plans."""
        if self.plan == 'basic':
            self.end_date = None  # No expiry for basic users
        elif not self.end_date:  # Only set end date if it's not already set
            self.end_date = self.start_date + timedelta(days=self.duration_days or 30)  # Default to 1 month
        super().save(*args, **kwargs)

    def is_active(self):
        """Check if the subscription is still valid (always True for Basic users)."""
        if self.plan == 'basic' or self.end_date is None:
            return True  # Basic users are always active
        return self.end_date >= now()


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
