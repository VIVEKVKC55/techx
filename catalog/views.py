from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Category, Product, ProductImage
from .forms import ProductForm
from django.db.models import Q


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
        queryset = Product.objects.filter(is_active=True)
        query = self.request.GET.get("q")
        category_slug = self.request.GET.get("category")

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(brand__icontains=query) |
                Q(specification__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["query"] = self.request.GET.get("q", "")
        context["category"] = self.request.GET.get("category", "")
        context["selected_category"] = self.request.GET.get("category", "")
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "default/catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
