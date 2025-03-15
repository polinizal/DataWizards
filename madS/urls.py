from django.urls import path
from .views import home, blog_list

urlpatterns = [
    path('', home, name='home'),  # Home page
    path('blog/', blog_list, name='blog-list'),  # Blog page
]