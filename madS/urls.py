from turtle import home
from django.urls import path
from .views import home


urlpatterns = [
    path('', home, name='home'),  # Home page

]