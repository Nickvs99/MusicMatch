from django.db import models
from django.contrib.auth.models import User

from jsonfield import JSONField

class Genre(models.Model):

    name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return f"{self.name}"
        
class Artist(models.Model):

    id = models.CharField(max_length=100, primary_key=True)

    name = models.CharField(max_length=50)

    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return f"{self.name}"

class Song(models.Model):

    id = models.CharField(max_length=100, primary_key=True)

    name = models.CharField(max_length=50)

    artists = models.ManyToManyField(Artist)

    def __str__(self):
        return f"{self.name}"

class SpotifyUser(models.Model):

    username = models.CharField(max_length=250, primary_key=True, default="")

    songs = models.ManyToManyField(Song, blank=True)

    last_updated = models.DateField(null=True, default=None)

    # Cashed results
    artist_count = JSONField(null=True, default=None)
    genre_count = JSONField(null=True, default=None)

    def __str__(self):
        return f"{self.username}"

class ExtendedUser(models.Model):
    """ Extends django's default User model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    access_token = models.CharField(blank=True, max_length=250)
    refresh_token = models.CharField(blank=True, max_length=250)

    spotify_account = models.OneToOneField(SpotifyUser, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username}"