from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Product
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.shortcuts import render
from customer.models import ProductView


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
