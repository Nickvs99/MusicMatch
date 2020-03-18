from django.db import models

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