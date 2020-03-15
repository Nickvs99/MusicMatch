from django.contrib import admin
from .models import *

class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'access_token', 'refresh_token']

admin.site.register(ExtendedUser, ExtendedUserAdmin)
