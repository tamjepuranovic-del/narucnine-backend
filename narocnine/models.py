from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class User(models.Model):
    ROLE_CHOICES = [('USER', 'User'), ('ADMIN', 'Admin')]
    username = models.CharField(max_length=255, unique=True)
    password_hash = models.TextField()
    firs_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.username


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Appointment(models.Model):
    TYPE_CHOICES = [('appointment', 'Appointment'), ('blackout', 'Blackout')]
    STATUS_CHOICES = [('active', 'Active'), ('cancelled', 'Cancelled')]

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    appointment_start_date = models.DateField()
    appointment_end_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
