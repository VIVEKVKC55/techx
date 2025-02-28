from django.urls import path
from .views import ProductCreateView, ProductListView

app_name="catalog"

urlpatterns = [
    path("product/add/", ProductCreateView.as_view(), name="product_create"),
    path("products/", ProductListView.as_view(), name="product_list"),
]
