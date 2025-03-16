from django.shortcuts import render, get_object_or_404
from .models import Survey, Choice, Article
import json


def home(request):
    articles = Article.objects.select_related('survey').prefetch_related('survey__tags').all()
    return render(request, 'home.html', {'articles': articles})

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
def view_articles(request):
    articles = Article.objects.select_related('survey').prefetch_related('survey__tags').all()
    return render(request, 'crm/view_articles.html', {'articles': articles})  # Use the correct template
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

def home(request):
    return render(request, 'crm/home.html')

def polls(request):
    return render(request, 'crm/polls.html')

def articles(request):
    return render(request, 'crm/articles.html')

def myPolls(request):
    return render(request, 'crm/myPolls.html')

def myArticles(request):
    return render(request, 'crm/myArticles.html')

def account(request):
    return render(request, 'crm/account.html')

def contribute(request):
    return render(request, 'crm/contribute.html')