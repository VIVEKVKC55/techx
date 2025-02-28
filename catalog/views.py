from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Product, ProductImage
from .forms import ProductForm

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "default/catalog/product_form.html"
    success_url = reverse_lazy("product_list")  # Update with the actual URL name

    def form_valid(self, form):
        product = form.save(commit=False)
        product.created_by = self.request.user  # Automatically assign the logged-in user
        product.save()
        
        # Handling multiple images
        images = self.request.FILES.getlist("images")
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        
        return redirect(self.success_url)


class ProductListView(ListView):
    model = Product
    template_name = "default/catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = "default/catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
