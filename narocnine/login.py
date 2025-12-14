from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password

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