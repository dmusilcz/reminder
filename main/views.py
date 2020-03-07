from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.


def home(request):
    return render(request, 'main/home.html')

def calendar(request):
    return render(request, 'main/calendar.html')

def docs(request):
    return render(request, 'main/docs.html')

def categories(request):
    return render(request, 'main/categories.html')