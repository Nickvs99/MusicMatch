from django.contrib import admin
from .models import ExtendedUser

# Register your models here.
class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ['user']

admin.site.register(ExtendedUser, ExtendedUserAdmin)
