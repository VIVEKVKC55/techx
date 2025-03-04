from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from django.utils.html import format_html
from django.urls import path
from .models import Subscription

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "username", "user_category", "date_joined", "is_active")
    list_filter = ("subscription__plan", "is_active")
    search_fields = ("email", "username")

    def user_category(self, obj):
        """Determine if user is Free or Paid and their plan type."""
        if hasattr(obj, "subscription"):
            if obj.subscription.plan == "premium":
                return "Paid - Category A"
            elif obj.subscription.plan == "scalable":
                return "Paid - Category B"
            return "Paid User"
        return "Free User"

    user_category.short_description = "User Type"

# Register the customized User model in admin
admin.site.unregister(User)  # Unregister default User model
admin.site.register(User, UserAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "duration_days", "is_approved", "pending_plan", "start_date", "end_date", "approve_button", "reject_button")
    list_filter = ("plan", "is_approved")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('approve/<int:subscription_id>/', self.admin_site.admin_view(self.approve_subscription), name="approve_subscription"),
            path('reject/<int:subscription_id>/', self.admin_site.admin_view(self.reject_subscription), name="reject_subscription"),
        ]
        return custom_urls + urls

    def approve_subscription(self, request, subscription_id):
        subscription = get_object_or_404(Subscription, id=subscription_id)
        if subscription.pending_plan:
            subscription.plan = subscription.pending_plan
            subscription.duration_days = subscription.pending_duration
            subscription.start_date = now()
            subscription.end_date = now() + timedelta(days=subscription.pending_duration)
            subscription.is_approved = True
            
            subscription.pending_plan = None
            subscription.pending_duration = None
            subscription.save()

            send_mail(
                "Subscription Approved",
                f"Dear {subscription.user.username},\n\nYour subscription has been upgraded to {subscription.plan} for {subscription.duration_days} days.\n\nBest Regards,\nSupport Team",
                "support@example.com",
                [subscription.user.email],
                fail_silently=True,
            )

            messages.success(request, "Subscription approved successfully.")
        return redirect('/admin/customer/subscription/')

    def reject_subscription(self, request, subscription_id):
        subscription = get_object_or_404(Subscription, id=subscription_id)
        if subscription.pending_plan:
            subscription.pending_plan = None
            subscription.pending_duration = None
            subscription.is_approved = False
            subscription.save()

            send_mail(
                "Subscription Upgrade Rejected",
                f"Dear {subscription.user.username},\n\nYour subscription upgrade request was rejected.\n\nBest Regards,\nSupport Team",
                "support@example.com",
                [subscription.user.email],
                fail_silently=True,
            )

            messages.warning(request, "Subscription upgrade request rejected.")
        return redirect('/admin/customer/subscription/')

    def approve_button(self, obj):
        if obj.pending_plan:
            return format_html('<a class="button" href="{}">Approve</a>', f"/admin/customer/subscription/approve/{obj.id}/")
        return "No pending request"

    def reject_button(self, obj):
        if obj.pending_plan:
            return format_html('<a class="button" style="color: red;" href="{}">Reject</a>', f"/admin/customer/subscription/reject/{obj.id}/")
        return "No pending request"

    approve_button.short_description = "Approve"
    reject_button.short_description = "Reject"

admin.site.register(Subscription, SubscriptionAdmin)
