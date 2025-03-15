from django import forms
from .models import Form, Question, Option

class FormCreationForm(forms.ModelForm):
    class Meta:
        model = Form
        fields = ['title']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['text']
