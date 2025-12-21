from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.parsers import JSONParser

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .login import AuthService

class LoginView(APIView):
    parser_classes = [JSONParser]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("Received username:", username, "password:", password)

        try:
            user = AuthService.login(username, password)
            tokens = AuthService.get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        except:
            print("Something went wrong", Response)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        try:
            user = AuthService.register(
                firs_name=data.get('firs_name'),
                last_name=data.get('last_name'),
                username=data.get('username'),
                email=data.get('email'),
                password=data.get('password')
            )
            tokens = AuthService.get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(
            {"message": "Account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

def homepage(request):
    return HttpResponse("Hello, world !")
