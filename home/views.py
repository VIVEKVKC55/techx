from django.shortcuts import render
from catalog.models import Category

def home_page(request):
    categories = Category.objects.filter(is_active=True, include_in_home=True).order_by("id")
    return render(request, 'default/home/home.html', {'categories': categories})
