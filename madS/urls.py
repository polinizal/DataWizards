from django.urls import path, include
from.import views
from .views import survey_results
urlpatterns = [
  path('', views.home, name='home'),
  path('blogs/', views.blogs, name='blogs'),
  path('blog-list/', views.bloglist, name='blog-list'),
  path('blog-details/', views.blog_details, name='blog-details'),
  path('create-blog/', views.create_blog, name='create-blog'),
  path('edit-blog/', views.edit_blog, name='edit-blog'),
  path('login/', views.login, name='login'),
  path('signup/', views.signup, name='signup'),
  path('survey/<int:survey_id>/results/', survey_results, name='survey_results'),
  path('index/', views.index, name='index'),
  path('userDataCollector/', views.userDataCollector, name='userDataCollector'),
  path('home/', views.home, name='home'),
  path('polls/', views.polls, name='polls'),
  path('articles/', views.articles, name='articles'),
  path('myPolls/', views.myPolls, name='myPolls'),
  path('account/', views.account, name='account'),
  path('myArticles/', views.myArticles, name='myArticles'),
  path('contribute/', views.contribute, name='contribute'),

]
