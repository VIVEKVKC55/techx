from django import forms
from .models import Subscription

# Define Subscription Pricing
PLAN_PRICES = {
    "premium": {30: 100, 180: 550, 365: 1000},  # Prices for Premium-A
    "scalable": {30: 120, 180: 650, 365: 1200},  # Prices for Premium-B
}
PLAN_CHOICE = [("premium", "Premium A"), ("scalable", "Premium B")]
DURATION_CHOICE = [(30, "30 Days"), (180, "180 Days"), (365, "365 Days")]

class SubscriptionUpgradeForm(forms.ModelForm):
    plan = forms.ChoiceField(choices=PLAN_CHOICE, required=True)
    duration = forms.ChoiceField(choices=DURATION_CHOICE, required=True)

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
