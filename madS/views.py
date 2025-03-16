from django.shortcuts import render, get_object_or_404
from .models import Survey, Choice
import json


def home(request):
   return render(request, 'crm/index.html')  # Updated path

def survey_results(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    questions = survey.questions.all()

    chart_data = []
    for question in questions:
        choices = question.choices.all()
        data = {choice.text: choice.votes.count() for choice in choices}
        chart_data.append({"question": question.text, "data": data})

    return render(request, 'crm/survey_chart.html', {  # Make sure this matches your template path
        "survey": survey,
        "chart_data_json": json.dumps(chart_data)
    })
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
