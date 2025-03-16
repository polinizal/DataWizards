from django.urls import path
from . import views
urlpatterns = [
    path('login-user', views.login_user, name='login'),
]