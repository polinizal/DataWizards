from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'crm/index.html')

def blogs(request):
    return render(request, 'crm/base.html')

def bloglist(request):
    return render(request, 'crm/blog_list.html')

def blog_details(request):
    return render(request, 'crm/blog_details.html')

def create_blog(request):
    return render(request, 'crm/create_blog.html')

def edit_blog(request):
    return render(request, 'crm/edit_blog.html')

def login(request):
    return render(request, 'crm/login.html')

def signup(request):
    return render(request, 'crm/signup.html')

def index(request):
    return render(request, 'crm/index.html')

def userDataCollector(request):
    return render(request, 'crm/userDataCollector.html')
