from django.urls import path, include
from.import views
urlpatterns = [
  path('', views.home, name='home'),
  path('blogs/', views.blogs, name='blogs'),
  path('post_detail/', views.post_detail, name='post_detail'),
  path('blog-details/', views.blog_details, name='blog-list'),
  path('create-blog/', views.create_blog, name='create-blog'),
  path('edit-blog/', views.edit_blog, name='edit-blog'),
  path('profile/', views.profile, name='profile'),
  path("form-builder/", views.form_builder, name="form_builder"),
  path("saved-forms/", views.form_list, name="form_list"),
  path('form/<int:form_id>/', views.form_detail, name='view_form'),
  path('save-form/', views.save_form, name='save_form'),  
]
