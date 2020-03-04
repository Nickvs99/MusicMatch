from django.db import models

# Create your models here.

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