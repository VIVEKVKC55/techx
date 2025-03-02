from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
from django.utils.timezone import now

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('scalable', 'Scalable'),
    ]
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='Basic')
    extra_slots = models.PositiveIntegerField(default=0)  # Purchased slots

    def __str__(self):
        return f"{self.user.username} - {self.get_plan_display()}"


class ProductView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viewed_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="user_views")
    viewed_at = models.DateTimeField(default=now)

    class Meta:
        unique_together = ("user", "product")  # Prevent duplicate views per user per product