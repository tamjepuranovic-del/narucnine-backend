from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import User, Location, Appointment

admin.site.register(User)
admin.site.register(Location)
admin.site.register(Appointment)
