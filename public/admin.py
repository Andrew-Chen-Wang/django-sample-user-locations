from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import User


class CustomUserAdmin(UserAdmin, OSMGeoAdmin):
    # Custom User Config
    model = User

    # Geo Config: https://github.com/django/django/blob/master/django/contrib/gis/admin/options.py
    map_srid = 4326
    units = 'm'


admin.site.register(User, CustomUserAdmin)
