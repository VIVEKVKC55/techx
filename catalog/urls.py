from django.urls import path
from .views import ProductCreateView, ProductListView, ProductDetailView

app_name="catalog"

urlpatterns = [
    path("product/add/", ProductCreateView.as_view(), name="product_create"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
