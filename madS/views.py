from django.shortcuts import render

def home(request):
    return render(request, 'crm/index.html')  # Updated path

def blog_list(request):
    return render(request, 'crm/blog.html')  # Updated path
