from django.contrib import admin
from .models import CustomUser, Tag, Survey, Question, Choice, Comment, Response

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    filter_horizontal = ('tags',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at', 'expires_at', 'is_active')
    search_fields = ('title', 'creator__username')
    list_filter = ('is_active', 'created_at', 'expires_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey')
    search_fields = ('text',)

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question')
    search_fields = ('text',)

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choice')
    search_fields = ('user__username', 'question__text')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'survey', 'created_at')
    search_fields = ('user__username', 'survey__title')
