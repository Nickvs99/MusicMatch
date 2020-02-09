from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """ Extends django's default User model."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    access_token = models.CharField(blank=True, max_length=250)

    refresh_token = models.CharField(blank=True, max_length=250)

    def __str__(self):
        return f"{self.user.username}"
