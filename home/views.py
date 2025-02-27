from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return HttpResponse("Hello, this is the home page!")
