from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Form, Question, Option
from .forms import FormCreationForm, QuestionForm, OptionForm
import json

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

def post_detail(request):
    return render(request, 'crm/post_detail.html')

def profile(request):
    return render(request, 'crm/profile.html')

def form_builder(request):
    return render(request, "crm/form_builder.html")

@csrf_exempt
def save_form(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form_id = data.get("id")

        if form_id:
            form = get_object_or_404(Form, id=form_id)
            form.title = data["title"]
            form.questions = json.dumps(data["questions"])  # Store as JSON
            form.save()
            return JsonResponse({"message": "Form updated successfully!"})
        else:
            new_form = Form.objects.create(
                title=data["title"], questions=json.dumps(data["questions"])
            )
            return JsonResponse({"message": "Form saved successfully!"})
    
    return JsonResponse({"error": "Invalid request"}, status=400)


def get_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    return JsonResponse({"title": form.title, "questions": json.loads(form.questions)})


def form_list(request):
    forms = Form.objects.all()
    return render(request, "crm/form_list.html", {"forms": forms})

def form_detail(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    return render(request, "crm/form_detail.html", {"form": form})