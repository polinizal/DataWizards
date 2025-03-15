from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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
@login_required
def save_form(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            form_form = FormCreationForm({"title": data["title"]})
            if form_form.is_valid():
                form = form_form.save(commit=False)
                form.creator = request.user
                form.save()

                for q in data.get("questions", []):
                    question_form = QuestionForm({"text": q["text"], "question_type": q["type"]})
                    if question_form.is_valid():
                        question = question_form.save(commit=False)
                        question.form = form
                        question.save()

                        for option_text in q.get("options", []):
                            option_form = OptionForm({"text": option_text})
                            if option_form.is_valid():
                                option = option_form.save(commit=False)
                                option.question = question
                                option.save()

                return JsonResponse({"message": "Form saved successfully!", "form_id": form.id}, status=201)
            else:
                return JsonResponse({"error": "Invalid form data"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def form_list(request):
    forms = Form.objects.all()
    return render(request, "crm/form_list.html", {"forms": forms})