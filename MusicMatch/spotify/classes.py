""" Classes used for views.py. These classes are not models."""

class Artist():
    """ An artist. This stores the artists name with its spotify id. 
        Count keeps track of how many times it is featured in users playlists."""

    def __init__(self, aritstname, artist_id):
        self.name = aritstname
        self.id = artist_id
        self.count = 1

    def __str__(self):
        return f"{self.name}, {self.count}"
    
    def __repr__(self):
        return f"'{self.__str__()}'"