from django.urls import path, include
from.import views
from .views import survey_results, save_survey, survey_list, survey_display, vote
urlpatterns = [
  path('', views.index, name='index'),
  path('blogs/', views.blogs, name='blogs'),
  path('blog-list/', views.bloglist, name='blog-list'),
  path('blog-details/', views.blog_details, name='blog-details'),
  path('create-blog/', views.create_blog, name='create-blog'),
  path('edit-blog/', views.edit_blog, name='edit-blog'),
  path('user_login/', views.user_login, name='user_login'),
  path('signup/', views.signup, name='signup'),
  path('survey/<int:survey_id>/results/', survey_results, name='survey_results'),
  #path('index/', views.index, name='index'),
  path('userDataCollector/', views.userDataCollector, name='userDataCollector'),
  path('home1/', views.home, name='home'),
  path('polls/', views.polls, name='polls'),
  path('articles/', views.articles, name='articles'),
  path('myPolls/', views.myPolls, name='myPolls'),
  path('account/', views.account, name='account'),
  path('myArticles/', views.myArticles, name='myArticles'),
  path('contribute/', views.contribute, name='contribute'),
  path("survey-builder/", views.survey_builder, name="survey_builder"),
  path('survey/<int:survey_id>/', views.survey_display, name='view_survey'),
  path('survey-list/', views.survey_list, name='survey_list'),
  path('save-survey/', views.save_survey, name='save_survey'),
  path("vote/<int:choice_id>/", vote, name="vote"),   
  path('home/', views.view_articles, name='view_articles'),
]
