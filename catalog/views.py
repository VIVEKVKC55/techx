from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Category, Product, ProductImage
from .forms import ProductForm
from django.db.models import Q
from django.contrib import messages
from django.utils.timezone import now, timedelta


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "default/catalog/product_form.html"
    success_url = reverse_lazy("user:user-products")  # Update with the actual URL name

    def form_valid(self, form):
        print(form)
        user = self.request.user
        time_threshold = now() - timedelta(hours=24)
        recent_product_count = Product.objects.filter(created_by=user, created_at__gte=time_threshold).count()

        if recent_product_count >= 2:
            messages.error(
                self.request, 
                "You can only add 2 products within 24 hours. "
                "If you want to add more products, please delete an old product or purchase subscription."
            )
            return redirect(self.request.path)  # Redirect to the same page to show the error

        # Save product with logged-in user
        product = form.save(commit=False)
        product.created_by = user
        product.save()
        
        # Handling multiple images
        images = self.request.FILES.getlist("images")
        for image in images:
            ProductImage.objects.create(product=product, image=image)

        messages.success(self.request, "Product added successfully!")
        return redirect(self.success_url)


class ProductListView(LoginRequiredMixin, ListView):
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

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "default/catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
