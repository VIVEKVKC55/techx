from django import forms
from .models import Subscription

# Define Subscription Pricing
PLAN_PRICES = {
    "premium": {30: 100, 90: 270, 365: 1000},  # Prices for Premium-A
    "scalable": {30: 150, 90: 400, 365: 1500},  # Prices for Premium-B
}

class SubscriptionUpgradeForm(forms.ModelForm):
    plan = forms.ChoiceField(choices=[("premium", "Premium"), ("scalable", "Scalable")], required=True)
    duration = forms.ChoiceField(choices=[(30, "30 Days"), (90, "90 Days"), (365, "365 Days")], required=True)

    class Meta:
        model = Subscription
        fields = ["plan", "duration"]

    def clean(self):
        cleaned_data = super().clean()
        plan = cleaned_data.get("plan")
        duration = int(cleaned_data.get("duration", 30))  # Default to 30 days if empty

        # Validate duration against the selected plan
        if plan not in PLAN_PRICES:
            raise forms.ValidationError("Invalid subscription plan selected.")

        if duration not in PLAN_PRICES[plan]:
            raise forms.ValidationError("Invalid duration selected.")

        return cleaned_data
