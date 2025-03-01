from django.urls import path
from .views import ProductCreateView, ProductListView, ProductDetailView

app_name="catalog"

urlpatterns = [
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("list/", ProductListView.as_view(), name="product_list"),
    path("<str:cat_slug>/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
