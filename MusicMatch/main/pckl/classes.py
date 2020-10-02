"""
Set of classes which are stored in the 
"""

import datetime

from django.contrib import messages

class SpotifyUser():

    def __init__(self, username, song_ids, artist_count, genre_count):

        self.username = username
        self.song_ids = song_ids
        self.artist_count = artist_count
        self.genre_count = genre_count

        self.update_last_updated()

        
    def update_last_updated(self):
        self.last_updated = datetime.date.today()
    
    def songs_check(self, request):
        """ Adds an info message when there are no songs. """
        
        if(len(self.song_ids) == 0):
            messages.info(request, f"No songs were found for {self.username}. Make sure that the playlists are set to public.")

class Artist():

    def __init__(self, id, name, genres):
        
        self.id = id
        self.name = name
        self.genres = genres

    def __str__(self):
        
        return f"id: {self.id}, name: {self.name}"

    