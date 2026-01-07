import os
from django.conf import settings

from django.contrib.messages.storage import session
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .booking import Booking
from .login import AuthService
from .models import Location, Appointment, User
from .appointmentinfo import get_appointment_info


class LoginView(APIView):
    parser_classes = [JSONParser]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("Received username:", username, "password:", password)

        try:
            user = AuthService.login(username, password)
            tokens = AuthService.get_tokens_for_user(user)
            request.session['current_user_id'] = user.user_id
            print("tokens:", tokens)
            return Response(tokens, status=status.HTTP_200_OK)
        except Exception as e:
            print("Login failed:", e)
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    parser_classes = [JSONParser]

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


# views.py
class DeleteAccountView(APIView):

    def delete(self, request):
        user_id = request.session.get('current_user_id')
        if not user_id:
            return Response({"detail": "Unauthorized"}, status=401)

        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=404)

        user.delete()
        request.session.flush()

        return Response(
            {"message": "Account deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

def homepage(request):
    popular_locations = Location.objects.filter(approved=True)[:3]
    user_id = request.session.get('current_user_id')

    if not user_id:
        return redirect('/')

    # Fetch the 3 most recent **normal appointments** for the logged-in user
    reserved_qs = (
        Appointment.objects
        .filter(user_id=user_id, type='appointment')[:3]
    )

    # Convert appointments to locations
    reserved_locations = [r.location for r in reserved_qs]

    # Fill up to 3 with None if there are fewer than 3 reservations
    while len(reserved_locations) < 3:
        reserved_locations.append(None)
    user = User.objects.get(user_id=user_id)
    profile_pic = user.profile_pic or 'static/narocnine/images/img.png'

    return render(request, 'homepage.html', {
        'popular_locations': popular_locations,
        'reserved_locations': reserved_locations,
        'profile_pic': profile_pic
    })


#TO BE POPRAVLJENO KAD SE NADJE VREMENA
def profile(request):
    if not request.session.get('current_user_id'):
        return redirect('/')
    user_id = request.session.get('current_user_id')
    user = User.objects.get(user_id=user_id)
    profile_pic = user.profile_pic or 'static/narocnine/images/img.png'
    return render(request, 'profil.html', {'profile_pic': profile_pic})

class ProfileView(APIView):
    parser_classes = [JSONParser]

    def get(self, request):
        user_id = request.session.get('current_user_id')
        if not user_id:
            return Response({"detail": "Unauthorized"}, status=401)

        user = User.objects.get(user_id=user_id)
        print(user)
        print(user.firs_name)

        return Response({
            "email": user.email,
            "username": user.username,
            "firs_name": user.firs_name,
            "last_name": user.last_name
        })

    def post(self, request):
        user_id = request.session.get('current_user_id')
        if not user_id:
            return Response({"detail": "Unauthorized"}, status=401)

        user = User.objects.get(user_id=user_id)
        user.email = request.data.get("email", user.email)
        user.username = request.data.get("username", user.username)
        user.firs_name = request.data.get("firs_name", user.firs_name)
        user.last_name = request.data.get("last_name", user.last_name)

        password = request.data.get("password_hash")
        if password and password != "******":
            user.set_password(password)

        user.save()
        return Response({"status": "success"})


@csrf_exempt
def upload_profile_picture(request):
    user_id = request.session.get('current_user_id')
    user = User.objects.get(user_id=user_id)

    if request.method == "POST" and request.FILES.get("profile_picture"):
        file = request.FILES["profile_picture"]
        file_path = f"media/profile_pics/{file.name}"

        save_path = os.path.join(settings.MEDIA_ROOT, "profile_pics", file.name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Save path to DB
        user.profile_pic = file_path
        user.save()

        return JsonResponse({"path": f"/{file_path}"})
    return JsonResponse({"error": "No file uploaded"}, status=400)


def rezervacija(request):
    if not request.session.get('current_user_id'):
        return redirect('/')
    locations = Location.objects.filter(approved=True)[:]
    return render(request,'rezervisanje.html',{'locations':locations})

def RezervacijaApi(request):
    print("api hit")

    user_id = request.session.get("current_user_id")
    if not user_id:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    location_id = int(request.POST.get("lokacija"))
    date_str = request.POST.get("date")
    start_time_str = request.POST.get("start_time")

    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
    except Exception:
        return JsonResponse({"error": "Invalid date or time"}, status=400)

    try:
        appointment = Booking.reserve(user_id, location_id, date, start_time)
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({
        "message": "Appointment successfully booked",
        "appointment_id": appointment.appointment_id
    })


def mestainfo(request, location_id):
    info = get_appointment_info(request.session, location_id)

    if not info:
        return render(request, 'mestainfo.html', {'error': "No reservation found."})

    return render(request, 'mestainfo.html', {'info': info})



def update_status(request, appointment_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    status = request.POST.get("status")
    if status not in ["active", "cancelled"]:
        return JsonResponse({"error": "Invalid status"}, status=400)

    try:
        appointment = Appointment.objects.get(appointment_id=appointment_id)
        appointment.status = status
        appointment.save()
    except Appointment.DoesNotExist:
        return JsonResponse({"error": "Appointment not found"}, status=404)

    return JsonResponse({"message": "Status updated successfully"})

def logout(request):
    request.session.flush()
    return redirect('/')