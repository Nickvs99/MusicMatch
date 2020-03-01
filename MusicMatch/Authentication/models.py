from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from spotify.models import Song


class UserProfile(models.Model):
    """ Extends django's default User model."""

    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    username = models.CharField(max_length=250, primary_key=True, default="")
    
    access_token = models.CharField(blank=True, max_length=250)

    refresh_token = models.CharField(blank=True, max_length=250)

    songs = models.ManyToManyField(Song, blank=True)

    last_updated = models.DateField(blank=True, default=now)

    def __str__(self):
        return f"{self.username}"
