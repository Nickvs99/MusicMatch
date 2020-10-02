from math import ceil
import os

from main.spotify.auth import get_sp
from main.spotify.data import get_playlists, get_songs
import main.pckl.helper as pckl_helper
import main.pckl.classes as pckl_classes
from main.util.dict import sort_dict_value

def write_data_to_server(username):
    """
    Cache the most important data from the spotify servers onto my server.

    These are:
    - Artist data
    - Spotify user data
    """
    
    sp = get_sp()

    song_ids = set([])
    missing_artist_ids = set([])

    artist_count = {}

    playlists = get_playlists(sp, username)
    for playlist in playlists:

        songs = get_songs(sp, username, playlist)

        for song in songs:
              
            # Check if the song has a track attribute. 
            # I guess local songs dont have them, but are still obtained with the spotipy id. 
            # These are only a very small percentage of the songs
            if not song['track']:
                continue
            
            song_id = song["track"]["id"]

            # No duplicate songs
            if song_id in song_ids:
                continue
            
            song_ids.add(song_id)

            for artist in song["track"]["artists"]:

                artist_id = artist["id"]
                artist_name = artist["name"]

                # Some artists dont have an spotify id. This is a very small percentage of the artists
                if artist_id is None:
                    continue
                
                path = pckl_helper.get_artist_file_path(artist_name)
                if not os.path.isfile(path):
                    missing_artist_ids.add(artist_id)

                if artist_name in artist_count:
                    artist_count[artist_name] += 1
                else:
                    artist_count[artist_name] = 1

    add_missing_artists_info(sp, missing_artist_ids)

    genre_count = {}
    for key, value in artist_count.items():

        path = pckl_helper.get_artist_file_path(key)
        artist_obj = pckl_helper.get_pickle_data(path)

        for genre in artist_obj.genres:

            if genre in genre_count:
                genre_count[genre] += value
            else:
                genre_count[genre] = value


    artist_count = sort_dict_value(artist_count)
    genre_count = sort_dict_value(genre_count)

    spotify_user = pckl_classes.SpotifyUser(username, song_ids, artist_count, genre_count)

    path = pckl_helper.get_user_file_path(username)
    pckl_helper.write_pickle_data(path, spotify_user)
        
def add_missing_artists_info(sp, artists_id):
    """ 
    Adds the genre information for new artists.
    Args:
        sp: spotipy object
        artists_id: set of strings
    """

    artists_id = list(artists_id)

    spotify_limit = 50
    count = 0
    # Since the limit of obtaining arists is 50, multiple requests have to be made.
    for i in range (ceil(len(artists_id)/spotify_limit)):
        
        # Get json response for n artists
        artists_response = sp.artists(artists_id[i * spotify_limit: (i + 1) * spotify_limit])

        for artist in artists_response["artists"]:
            
            genres = []
            for genre in artist["genres"]:
                
                genres.append(genre) 

            art = pckl_classes.Artist(artist["id"], artist["name"], genres)

            path = pckl_helper.get_artist_file_path(artist["name"])
            pckl_helper.write_pickle_data(path, art)

            count += 1
