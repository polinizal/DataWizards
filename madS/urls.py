from django.urls import path
from .views import home, blog_list, blog_detail, blog_create, blog_update, blog_delete

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('blogs/', blog_list, name='blog_list'),        # List all blogs
    path('blogs/<int:blog_id>/', blog_detail, name='blog_detail'),  # View a blog
    path('blogs/create/', blog_create, name='blog_create'),  # Create a new blog
    path('blogs/<int:blog_id>/edit/', blog_update, name='blog_update'),  # Edit blog
    path('blogs/<int:blog_id>/delete/', blog_delete, name='blog_delete'),  # Delete blog
]