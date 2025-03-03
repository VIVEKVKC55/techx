from django.contrib import admin
from django.contrib.auth import get_user_model
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
    list_display = ("user", "plan", "duration_days", "start_date", "end_date", "is_active_status")
    list_filter = ("plan", "duration_days", "end_date")
    search_fields = ("user__username", "user__email")

    def is_active_status(self, obj):
        return obj.is_active()
    
    is_active_status.boolean = True
    is_active_status.short_description = "Active"

admin.site.register(Subscription, SubscriptionAdmin)
