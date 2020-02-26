from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User


class CustomUserAdmin(OSMGeoAdmin):
    # Custom User Config
    model = User
    add_form = UserCreationForm
    form = UserChangeForm

    list_display = ['username', 'first_name', 'last_name', 'location']
    readonly_fields = ['last_login', 'date_joined']

    def get_form(self, request, obj=None, change=False, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super(CustomUserAdmin, self).get_form(request, obj, **defaults)

    # Geo Config: https://github.com/django/django/blob/master/django/contrib/gis/admin/options.py
    # map_srid = 4326
    # units = 'm'


admin.site.register(User, CustomUserAdmin)
