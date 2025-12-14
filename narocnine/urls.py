from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import LoginView, RegisterView

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
]