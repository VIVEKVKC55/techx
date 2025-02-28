from django.urls import path
from .views import ProductCreateView, ProductListView, ProductDetailView, CategoryProductListView, ProductSearchView

app_name="catalog"

urlpatterns = [
    path("product/add/", ProductCreateView.as_view(), name="product_create"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path('category/<str:slug>/', CategoryProductListView.as_view(), name='category_products'),
    path("search/", ProductSearchView.as_view(), name="product_search"),
]
