from django.urls import path, include
from.import views
urlpatterns = [
  path('', views.home, name='home'),
  path('blogs/', views.blogs, name='blogs'),
  path('blog-list/', views.bloglist, name='blog-list'),
  path('blog-details/', views.blog_details, name='blog-list'),
  path('create-blog/', views.create_blog, name='create-blog'),
  path('edit-blog/', views.edit_blog, name='edit-blog'),


  
]
