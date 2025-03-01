from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from catalog.models import Product


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
