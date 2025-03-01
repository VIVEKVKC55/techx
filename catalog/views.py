from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Category, Product, ProductImage
from .forms import ProductForm
from django.db.models import Q
from django.contrib import messages
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from customer.models import ProductView  # Import the new model


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "default/catalog/product_form.html"
    success_url = reverse_lazy("user:user-products")  # Update with the actual URL name

    def get_max_products(self, user):
        """Returns the max number of products a user can add in 24 hours."""
        if hasattr(user, 'subscription'):
            if user.subscription.plan == "scalable":
                return user.subscription.extra_slots + 10  # Base 10 + Purchased Slots
            elif user.subscription.plan == "premium":
                return 10  # 10 products per day for premium users
        return 2  # Default limit for free users

    def form_valid(self, form):
        user = self.request.user
        time_threshold = now() - timedelta(hours=24)
        recent_product_count = Product.objects.filter(created_by=user, created_at__gte=time_threshold).count()
        max_products = self.get_max_products(user)

        # Check if the user has exceeded their limit
        if max_products != float('inf') and recent_product_count >= max_products:
            messages.error(
                self.request, 
                f"You have reached your daily limit of {max_products} products. "
                "Buy more slots or upgrade your plan."
            )
            return redirect("subscription:buy-slots")  # Redirect to slot purchase page

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

    def get_max_views(self, user):
        """Returns the max number of product views allowed per day based on subscription."""
        if hasattr(user, 'subscription') and user.subscription.plan in ["premium", "scalable"]:
            return float('inf')  # Unlimited for premium/scalable users
        return 5  # Default limit for free users

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        user = request.user
        time_threshold = now() - timedelta(hours=24)

        # Count views within the last 24 hours
        recent_views_count = ProductView.objects.filter(user=user, viewed_at__gte=time_threshold).count()
        max_views = self.get_max_views(user)

        if recent_views_count >= max_views:
            messages.error(request, f"You have reached your daily limit of {max_views} product views.")
            return JsonResponse({"error": "Daily limit reached. Please upgrade your plan or come back tomorrow."}, status=403)

        # Store or update the product view in the database
        ProductView.objects.update_or_create(
            user=user, product=product,
            defaults={"viewed_at": now()}  # Always update the timestamp
        )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Pass viewed products (last 24 hours) to the template."""
        context = super().get_context_data(**kwargs)
        time_threshold = now() - timedelta(hours=24)
        viewed_products = Product.objects.filter(user_views__user=self.request.user, user_views__viewed_at__gte=time_threshold)
        context["viewed_products"] = viewed_products
        return context
