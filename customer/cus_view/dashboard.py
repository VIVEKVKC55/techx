from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Product
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.shortcuts import render, redirect
from customer.models import ProductView, Subscription
from django.contrib import messages


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "default/customer/dashboard/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'profile'
        return context


class UserProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "default/customer/dashboard/products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(created_by=self.request.user)

class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = "default/customer/dashboard/change_password.html"  # Update with your template path
    success_url = reverse_lazy("user:profile")  # Redirect to profile page after password change
    success_message = "Your password has been successfully updated!"


class UserViewedProductsView(LoginRequiredMixin, View):
    def get(self, request):
        """Retrieve products the logged-in user has viewed."""
        viewed_products = Product.objects.filter(user_views__user=request.user).distinct()

        return render(request, "default/customer/dashboard/viewed_products.html", {"viewed_products": viewed_products})


class UsersWhoViewedMyProductsView(LoginRequiredMixin, View):
    def get(self, request):
        """Retrieve users who have viewed my products."""
        my_products = Product.objects.filter(created_by=request.user)
        product_views = ProductView.objects.filter(product__in=my_products).select_related("user", "product")

        user_product_views = {}
        for view in product_views:
            if view.product not in user_product_views:
                user_product_views[view.product] = []
            user_product_views[view.product].append(view.user)

        return render(request, "default/customer/dashboard/users_who_viewed_my_products.html", {"user_product_views": user_product_views})


from customer.forms import SubscriptionUpgradeForm, PLAN_PRICES

class SubscriptionUpgradeView(LoginRequiredMixin, View):
    template_name = "default/customer/dashboard/upgrade.html"

    def get(self, request, *args, **kwargs):
        """Render the upgrade form with the user's current subscription."""
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        form = SubscriptionUpgradeForm(initial={"plan": subscription.pending_plan or subscription.plan})
        
        return render(request, self.template_name, {
            "form": form,
            "subscription": subscription,
            "plan_prices": PLAN_PRICES,
        })

    def post(self, request, *args, **kwargs):
        """Handle subscription upgrade requests via form."""
        subscription, created = Subscription.objects.get_or_create(user=request.user)
        form = SubscriptionUpgradeForm(request.POST)

        if form.is_valid():
            new_plan = form.cleaned_data["plan"]
            new_duration = int(form.cleaned_data["duration"])
            price = PLAN_PRICES[new_plan][new_duration]

            # Prevent downgrade to basic plan
            if subscription.plan in ["scalable","premium-b"] and new_plan == "premium":
                messages.error(request, "Downgrade to the Premium plan is not allowed.")
                return redirect("user:subscription_upgrade")

            # Save pending request for admin approval
            subscription.pending_plan = new_plan
            subscription.pending_duration = new_duration
            subscription.is_approved = False
            subscription.save()

            messages.success(request, f"Your upgrade request to {new_plan} for {new_duration} days at ${price} is pending admin approval.")
            return redirect("user:subscription_upgrade")

        return render(request, self.template_name, {
            "form": form,
            "subscription": subscription,
            "plan_prices": PLAN_PRICES,
        })