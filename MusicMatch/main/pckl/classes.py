"""
Set of classes which are stored in the 
"""


import datetime

class SpotifyUser():

    def __init__(self, song_ids, artist_count, genre_count):

        self.song_ids = song_ids
        self.artist_count = artist_count
        self.genre_count = genre_count

        self.update_last_updated()

        
    def update_last_updated(self):
        self.last_updated = datetime.date.today()

class Artist():

    def __init__(self, id, name, genres):
        
        self.id = id
        self.name = name
        self.genres = genres

    def __str__(self):
        
        return f"id: {self.id}, name: {self.name}"

    