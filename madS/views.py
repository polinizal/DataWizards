from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now, timedelta
from .models import Survey, Choice, Question, CustomUser, Tag
from .forms import SurveyForm, QuestionForm, ChoiceForm

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


from django.shortcuts import render, redirect
from .models import Survey, Question, Choice, Tag
from .forms import SurveyForm

from django.shortcuts import render, redirect
from .models import Survey, Question, Choice, Tag
from .forms import SurveyForm

def survey_builder(request):
    if request.method == "POST":
        print("SAVE SURVEY FUNCTION TRIGGERED")  # Debugging statement
        survey_form = SurveyForm(request.POST)
        
        if survey_form.is_valid():
            survey = survey_form.save(commit=False)
            survey.creator = None  # No user required
            survey.save()

            # Handle question
            question_text = request.POST.get('question')
            if question_text:
                question = Question.objects.create(survey=survey, text=question_text)

                # Handle choices for the question
                for i in range(1, 5):  # Assume max 4 choices
                    choice_text = request.POST.get(f'option_text_{i}')
                    if choice_text:
                        Choice.objects.create(question=question, text=choice_text)

            # ✅ Save selected tags
            selected_tags = request.POST.getlist("tags")  # Get selected tag IDs
            if selected_tags:
                survey.tags.set(selected_tags)  # Correct way to set ManyToManyField

            return redirect('crm/survey_list')  # Redirect to list of surveys

    else:
        survey_form = SurveyForm()
        available_tags = Tag.objects.all()  # ✅ Fetch available tags

    return render(request, "crm/survey_builder.html", {
        "survey_form": survey_form,
        "available_tags": available_tags  # ✅ Pass tags to the template
    })



def save_survey(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        duration_days = int(request.POST.get("duration", 7))  # Default to 7 days

        if not title or not description:
            return render(request, "survey_builder.html", {"error": "Title and Description are required"})

        # ✅ Calculate expiration date
        expires_at = now() + timedelta(days=duration_days)

        # ✅ Create the Survey
        survey = Survey.objects.create(
            title=title,
            description=description,
            expires_at=expires_at
        )

        # ✅ Process questions
        question_text = request.POST.get("question")
        if question_text:
            question = Question.objects.create(survey=survey, text=question_text)

            # ✅ Process choices
            for i in range(1, 5):  # Assume max 4 choices
                choice_text = request.POST.get(f'option_text_{i}')
                if choice_text:
                    Choice.objects.create(question=question, text=choice_text)

        # ✅ Save selected tags
        selected_tags = request.POST.get("tags")  # Tags are sent as a comma-separated string
        if selected_tags:
            tag_ids = [int(tag_id) for tag_id in selected_tags.split(",") if tag_id.isdigit()]
            survey.tags.set(Tag.objects.filter(id__in=tag_ids))  # Attach selected tags to the survey

        return redirect("survey_list")  # Redirect to survey list

    return render(request, "survey_builder.html", {"error": "Invalid request"})


def get_survey(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    return JsonResponse({"title": survey.title, "questions": json.loads(survey.questions)})


def survey_list(request):
    """List all active surveys"""
    surveys = Survey.objects.filter(is_active=True)  # Only show active surveys
    return render(request, "crm/survey_list.html", {"surveys": surveys})  # ✅ This must match your template name!


def survey_display(request, survey_id):
    """Fetches the full survey with questions and choices."""
    survey = get_object_or_404(Survey, id=survey_id)

    # Prefetch related questions and choices to avoid multiple queries
    questions = Question.objects.filter(survey=survey).prefetch_related("choices")

    return render(request, "crm/survey_display.html", {"survey": survey, "questions": questions})

def create_survey(request):
    form = SurveyForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("survey_list")
    return render(request, "create_survey.html", {"form": form})


@csrf_exempt
def vote(request, choice_id):
    """Allow a user to vote for a choice"""
    if request.method == "POST":
        try:
            user = request.user  # Ensure user is authenticated
            choice = get_object_or_404(Choice, id=choice_id)

            # Enforce one vote per question
            if Choice.objects.filter(question=choice.question, votes=user).exists():
                return JsonResponse({"error": "You have already voted on this question."}, status=400)

            choice.votes.add(user)
            return JsonResponse({"message": "Vote recorded successfully!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)
