from django.shortcuts import render
from rest_framework.views import APIView

from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginView, RegisterView, DeleteAccountView, homepage, profile, ProfileView, rezervacija, \
    RezervacijaApi, mestainfo, update_status, logout

urlpatterns = [

    path('', lambda request: render(request, 'login.html'), name='login-page'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('api/delete/', DeleteAccountView.as_view(), name='delete'),
    path('homepage/', homepage, name='homepage'),
    path('profile/', profile, name='profil'),
    path('api/profile/', ProfileView.as_view(), name='api-profile'),
    path('rezervisanje/', rezervacija, name='rezervisanje'),
    path('api/rezervacija/', RezervacijaApi, name='rezervacija_api'),
    path('mestainfo/<int:location_id>/', mestainfo, name='mestainfo'),
    path('api/update-status/<int:appointment_id>/', update_status, name='update_status'),
    path('logout/', logout, name='logout'),

]