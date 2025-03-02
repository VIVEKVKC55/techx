from django.db import models
from django.contrib.auth.models import User

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
