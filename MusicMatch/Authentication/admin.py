from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    """ Creates columns for UserProfile. """
    list_display = ['username', 'access_token', 'refresh_token']

admin.site.register(UserProfile, UserAdmin)
