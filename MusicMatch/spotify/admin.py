from django.contrib import admin
from .models import *

# Register your models here.
class SongAdmin(admin.ModelAdmin):
    list_display = ["name"]

class GenreAdmin(admin.ModelAdmin):
    list_display = ["name"]

class ArtistAdmin(admin.ModelAdmin):
    list_display = ["name"]  

admin.site.register(Song, SongAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Artist, ArtistAdmin)
