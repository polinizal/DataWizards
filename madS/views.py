from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog


def home(request):
    return render(request, 'crm/index.html')  # Updated path

