from django.shortcuts import render

from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginView, RegisterView, DeleteAccountView, homepage

urlpatterns = [

    path('', lambda request: render(request, 'login.html'), name='login-page'),
    path('login/', LoginView.as_view(), name='login'),

    path('register/', RegisterView.as_view(), name='register'),
   # path('api/delete/', DeleteAccountView.as_view(), name='delete'),
    path('homepage/', homepage, name='homepage'),


]