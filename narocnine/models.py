from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.

class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    ROLE_CHOICES = [('USER', 'User'), ('ADMIN', 'Admin')]
    username = models.CharField(max_length=255, unique=True)
    password_hash = models.TextField()
    firs_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users'
        managed = False

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.username

    @property
    def id(self):
        return self.user_id


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_by = models.BigIntegerField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'locations'
        managed = False

    @property
    def creator(self):
        from .models import User
        return User.objects.get(user_id=self.created_by)

    def __str__(self):
        return f"{self.name} - {self.address}"

class Appointment(models.Model):
    TYPE_CHOICES = [('appointment', 'Appointment'), ('blackout', 'Blackout')]
    STATUS_CHOICES = [('active', 'Active'), ('cancelled', 'Cancelled'), ('not active', 'Not Active')]

    #jer django voli da bude glup za fk i pk
    appointment_id = models.BigAutoField(primary_key=True)
    location_id = models.BigIntegerField()
    user_id = models.BigIntegerField(null=True, blank=True)

    appointment_start_date = models.DateField()
    appointment_end_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)


    #zbog djangovog assuming naziva vrsta u tabeli.
    class Meta:
        db_table = 'appointments'
        managed = False

    @property
    def location(self):
        from .models import Location
        return Location.objects.get(id=self.location_id)

    @property
    def user(self):
        from .models import User
        return User.objects.get(user_id=self.user_id)

    @property
    def appointment(self):
        return self.appintment_id