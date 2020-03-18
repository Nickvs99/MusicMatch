from django.contrib import admin
from .models import *

class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'spotify_account']

admin.site.register(ExtendedUser, ExtendedUserAdmin)
