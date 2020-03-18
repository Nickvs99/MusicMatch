from django.db import models
from django.contrib.auth.models import User

from spotify.models import SpotifyUser

class ExtendedUser(models.Model):
    """ Extends django's default User model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    access_token = models.CharField(blank=True, max_length=250)
    refresh_token = models.CharField(blank=True, max_length=250)

    spotify_account = models.OneToOneField(SpotifyUser, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user.username}"
