from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password


class AuthService:

    @staticmethod
    def login(username, password):

        # proverava username, ako nije u tabeli onda exception
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Exception('User not found')

        # proverava password
        if not user.check_password(password):
            raise Exception('Incorrect password')

        return user

    def get_toknes_for_user(user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'username': user.username,
            'role': user.role
        }

    def register(username, password, firs_name, last_name, email):

        #gleda jel username postoji
        if User.objects.filter(username=username).exists():
            raise Exception('User with this username already exists')
        #gleda jel email postoji
        if User.objects.filter(email=email).exists():
            raise Exception('User with this email already exists')

        user = User(username=username, password_hash=make_password(password) ,first_name=firs_name, last_name=last_name, email=email)
        user.save()
        return user



