import os
import json
from math import ceil
import requests
import datetime

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2

from django.contrib.auth.models import User
from django.core.mail import send_mail

from .models import *
from .util import get_env_var

""" A set of functions used in views.py. """

def get_playlists(sp, username):
    """
    Returns all playlist items for a given username.
    Args:
        username: str
    Returns:
        playlists: json response
        
    """

    return sp.user_playlists(username)['items']

def get_songs(sp, username, playlist):
    """
    Returns all songs from a playlist.
    Args:
        sp: spotipy object
        username: str
        playlist: json response

    Returns:
        songs: list of json responses
    """

    track_count = playlist['tracks']['total']

    songs = []
    limit_spotipy_request = 100

    for i in range (ceil(track_count/limit_spotipy_request)):

        # Get the tracks from the playlist.
        # Since spotipy has a limit on the number of tracks you can get per request. This step is repeated n times.
        song_response = sp.user_playlist_tracks(username, playlist_id=playlist['id'], limit = limit_spotipy_request, offset=i * 100)
        
        for song in song_response['items']:
            songs.append(song)

    return songs

def get_data(user):
    """ 
    Gets the data from all the songs from a user
    Args:
        user: SpotifyUser object
    Returns:
        artist_count: dict, keys:artists (str), value: count (int)
        genre_count: dict, keys:artists (str), value: count (int)
    """
    
    # Keeps track of how many times an artist/genre is featured in the public playlists
    artists_count = {}
    genre_count = {}

    for song in user.songs.all():

        for artist in song.artists.all():

            if artist.name in artists_count:
                artists_count[artist.name] += 1

            else:
                artists_count[artist.name] = 1

            for genre in artist.genres.all():

                if genre.name in genre_count:
                    genre_count[genre.name] += 1

                else:
                    genre_count[genre.name] = 1
    
    artists_count = sort_dict_value(artists_count)
    genre_count = sort_dict_value(genre_count)

    return artists_count, genre_count

def get_sp():
    """
    Obtains a spotipy object. With this object you can make calls to
    the spotify database.
    Returns:
        spotipy object
    """
    # Not sure if this is needed for every request
    credentials = oauth2.SpotifyClientCredentials(
            client_id=get_env_var("CLIENT_ID"),
            client_secret=get_env_var("CLIENT_SECRET")
        )
    token = credentials.get_access_token()

    sp = spotipy.Spotify(auth=token)

    return sp

def get_total_dict_value(dictionary):
    """
    Returns the sum of all values in a dictionary.
    Args: dictionary, value has to be an int
    Returns: int
    """

    total = 0
    for value in dictionary.values():
        total += value

    return total

def get_auth_sp(user):
    """
    Get an authorized spotipy object for the user.
    Args:
        user: ExtendedUser object
    Returns:
        authorized spotipy object
    """

    refresh_access_token(user)

    sp = spotipy.Spotify(auth=user.access_token)

    return sp

def create_playlist(sp, username, usernames, songs_id):
    """
    Creates an spotify playlist with the songs. This playlist is stored on the account of username.
    Args:
        sp: spotipy object
        username: str
        usernames: list of strings
        songs_id: list of strings.
    """
    
    playlist_name  = f"Music Match - {usernames[0]} - {usernames[1]}"
    playlist = sp.user_playlist_create(username, playlist_name, public = False)

    sp_limit = 100
    for i in range(ceil(len(songs_id)/100)):
        sp.user_playlist_add_tracks(username, playlist['id'], songs_id[i * 100:(i + 1) * 100])

def refresh_access_token(user):
    """
    Refreshes the access token for the user.
    Args:
        user: ExtendedUser object
    """

    # Refresh access token
    API_BASE = 'https://accounts.spotify.com'
    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"refresh_token",
        "refresh_token": user.refresh_token,
        "client_id":get_env_var("CLIENT_ID"),
        "client_secret":get_env_var("CLIENT_SECRET")
        })

    res_body = res.json()
    access_token =  res_body.get("access_token")

    user.access_token = access_token
    user.save()

def user_exists(sp, username):
    """
    Checks if a user exists. Returns True if the user exists, else returns False.
    Args:
        sp: spotipy object
        username: str
    Returns: bool
    """

    try:
        sp.user(username)

        return True
    except:

        return False

def get_frequent_keys(dict1, dict2):
    """ 
    Returns a sorted list of keys based on the compared ranking between two dictionaries.
    params:
        dict1, dict2: dictionary whose values have to be floats or ints
    Returns:
        list of strings
    """

    user1_total = get_total_dict_value(dict1)
    user2_total = get_total_dict_value(dict2)

    in_common_artists = {}

    for key in dict1:
        if key in dict2:
            user1_count = dict1[key]
            user2_count = dict2[key]
            in_common_artists[key] = (user1_count / user1_total) * (user2_count / user2_total)
            
    return list(sort_dict_value(in_common_artists).keys())

def sort_dict_value(dictionary):
    """
    Sort a dictionary based on the values from high to low.
    Args: dictionary, value has to be an integer or float
    Returns: sorted dictionary
    """

    return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))

def get_n_dict_and_count(n, keys, dict1, dict2):
    """
    Returns the first n artists, and their respective count for user1 and user2.
    Args:
        n: int, the number of returned items
        keys: list of str
        dict1, dict2: dictionary
    Returns:
        keys: list of str
        user1_count: dictionary, with only the keys from keys
        user2_count: dictionary, with only the keys from keys
    """

    keys = keys[:n]
    user1_count, user2_count = [], []
    for key in keys:

        user1_count.append(dict1[key])
        user2_count.append(dict2[key])

    return keys, user1_count, user2_count

def write_data_to_db(username):
    """
    Writes the songs, artists and genres from username to the database.
    Adds a relationship between the songs and the SpotifyUser.
    Args: username, str
    """

    sp = get_sp()

    user =  SpotifyUser.objects.filter(username=username).first()
    if user is None:
        user = SpotifyUser(username=username)
        user.save()
    
    user.last_updated = datetime.date.today()
    user.save()

    # dict with arists who are not yet in the database. These are grouped together,
    # since this will result in less calls to the spotify database.
    # key: artist id, value: Artist object
    missing_artists_info = {}

    playlists = get_playlists(sp, username)
    for playlist in playlists:

        songs = get_songs(sp, username, playlist)

        for song in songs:
            
            song_id = song["track"]["id"]
            
            if Song.objects.filter(pk = song_id).exists():

                user.songs.add(Song.objects.filter(pk = song_id).first())

                continue
  
            # Check if the song has a track attribute. 
            # I guess local songs dont have them, but are still obtained with the spotipy id. 
            # These are only a very small percentage of the songs
            if not song['track']:
                continue

            new_song = Song(id=song_id, name=song["track"]["name"])
            new_song.save()

            user.songs.add(new_song)

            artists = []
            for artist in song["track"]["artists"]:

                artist_id = artist["id"]

                # Some artists dont have an spotify id. This is a very small percentage of the artists
                if artist_id is None:
                    continue
                
                artist_obj = Artist.objects.filter(pk = artist_id).first()
                
                # Check if the artist exists in the database
                if not artist_obj:
                    
                    if artist_id not in missing_artists_info:
                        artist_obj = Artist(id=artist_id, name=artist["name"])
                        artist_obj.save()

                        missing_artists_info[artist_id] = artist_obj
                    
                    else:
                        artist_obj = missing_artists_info[artist_id]

                artists.append(artist_obj)

            new_song.artists.add(*artists)

    add_missing_artists_info(sp, missing_artists_info)

def add_missing_artists_info(sp, artists_dict):
    """ 
    Adds the genre information for new artists.
    Args:
        sp: spotipy object
        artists_dict: dict, key = artist_id, value = Artist object
    """
    
    # Get all missing artists ids
    artists_id = list(artists_dict.keys())

    spotify_limit = 50
    count = 0
    # Since the limit of obtaining arists is 50, multiple requests have to be made.
    for i in range (ceil(len(artists_id)/spotify_limit)):
        
        # Get json response for n artists
        artists_response = sp.artists(artists_id[i * spotify_limit: (i + 1) * spotify_limit])

        for artist in artists_response["artists"]:
            
            genres = []
            for genre in artist["genres"]:
                
                # Check if genre already exists
                genre_obj = Genre.objects.filter(pk = genre).first()
                if not genre_obj:

                    genre_obj = Genre(name = genre)
                    genre_obj.save()

                genres.append(genre_obj) 

            artist_obj = artists_dict[artists_id[count]]
            artist_obj.genres.add(*genres)

            count += 1

def send_email(subject, message, recipients):
    """
    Sends email
    Args:
        subject: str
        message: str
        recipients: list of str
    """

    try:
        send_mail(
                subject,
                message,
                get_env_var("EMAIL_HOST_USER"),
                recipients,
                fail_silently = False
            )
    except:
        print( '\n'.join((
            "Possible solutions:",
            " - Make sure your email and password are the right combination.",
            " - Turn on less secure apps on your google account, visit https://myaccount.google.com/lesssecureapps?pli=1 to turn the feature on.",
            " - Have a stable internet connection."
        )))

def get_total_songs(user):

    return user.songs.count()

def get_total_artists(user):

    return len(user.artist_count)

def get_total_genres(user):

    return len(user.genre_count)

def get_dict_comparison(dict1, dict2):
    """ 
    Compares two dictionaries based on their keys and values
    Args:
        dict1, dict2: dict{key: string, value: int/float}
    Returns:
        list_coparison: list[string, list[float, float]], sorted decreasingly 
            based on the values from dict1 and dict2
    """

    user1_total = get_total_dict_value(dict1)
    user2_total = get_total_dict_value(dict2)

    # Create an dictionary where a dict key has a certain comparison value
    dict_comparison = {}
    for key in dict1:
        if key in dict2:
            user1_count = dict1[key]
            user2_count = dict2[key]
            dict_comparison[key] = (user1_count / user1_total) * (user2_count / user2_total)
    
    # sort the dictionary based on the comparison value
    dict_comparison = sort_dict_value(dict_comparison)

    # replace comparison value with the initial 
    for key in dict_comparison:
        dict_comparison[key] = [dict1[key], dict2[key]]

    return dict_comparison

def get_unique_songs(songs1, songs2):
    """
    Get the total number of unique songs across two song query sets.
    Args:
        songs1, songs2: Queryset of songs

    Returns:
        int: The total number of unique songs
    """

    song_count = songs1.count()

    for song in songs2.all():
        if not songs1.filter(id=song.id).exists():
            song_count += 1

    return song_count

def get_shared_songs(songs1, songs2):
    """
    Get the total number of songs which occur in both querysets.
    Args:
        songs1, songs2: Queryset of songs

    Returns:
        int: The total number of shared songs
    """

    song_count = 0
    for song in songs2.all():
        if songs1.filter(id=song.id).exists():
            song_count += 1

    return song_count

def get_unique_keys(dict1, dict2):
    """
    Get the total number of unique keys in the dictionaries.
    Args:
        dict1, dict2: dict
    Returns:
        int: Total number of unique keys
    """

    key_count = len(dict1);

    for key in dict2.keys():
        if key not in dict1:
            key_count += 1
    
    return key_count

def get_shared_keys(dict1, dict2):
    """
    Get the total number of shared keys across both dictionaries.
    Args:
        dict1, dict2: dict
    Returns:
        int: Total number of shared keys
    """
    key_count = 0;

    for key in dict2.keys():
        if key in dict1:
            key_count += 1
    
    return key_count