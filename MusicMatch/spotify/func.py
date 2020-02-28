import os
import json

from math import ceil
from operator import itemgetter, attrgetter
import requests

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2

from .classes import Artist
from .genres import popular_genres
from Authentication.models import UserProfile
from spotify.models import Artist, Song, Genre

from django.contrib.auth.models import User
from django.contrib import messages

from utils.utils import get_env_var

""" A set of functions used in views.py. """

def print_json(json_response):
    """ Prints the json response in a human readable form."""

    print(json.dumps(json_response, indent=4))

def print_dic(dic):
    """ Prints the items from dic on a new line for each. Makes it more human readable."""

    for key, value in dic.items():
        print(key, value)

def get_playlists(sp, username):
    """ Returns all playlist items. """

    return sp.user_playlists(username)['items']

def get_songs(sp, username, playlist):
    """ Returns all songs from a playlist."""

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

def get_artists_from_song(song):
    """ Returns all artists from a song."""

    artists_id = []

    for artist in song['track']['artists']:

        # Some very small artists do not have an id, those artists are not 
        # used for the stats or comparison.
        if artist['id'] != None:
            artists_id.append(artist)

    return artists_id

def get_artist_count(user_profile):
    """ Returns how many times an artist occurs in the usernames playlists. 
        Return:
            artist_count: dictionary, keys:artists, value:count
    """
    
    # Keeps track of how many times an artist/genre is featured in the public playlists
    artists_count = {}
    genre_count = {}

    for song in user_profile.songs.all():

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
    
    return artists_count, genre_count

def get_n_heighest_from_dict(dictionary, n):
    """ 
    Sorts the artists_count from high to low and return the nth most frequent artists.
    Args:
        dictionary (dictionary): The dictionary whose keys and values are sorted.
        n (int): Get the top n values.
    
    """
    # TODO better function name

    # Sort dic from high to low, based on the value
    sorted_dict = sort_dict_value(dictionary)

    # Get the n heightest values and their respective key. Store these in a dictionay
    frequent_dictionary = {}
    count = 0
    for key in sorted_dict:
        frequent_dictionary[key] = sorted_dict[key]

        count += 1
        if count == n:
            break


    return frequent_dictionary

def get_artists_id(artists_count):
    """ Get the all artists id from artist_count. """

    artists_id = []
    for artist in artists_count.values():
        artists_id.append(artist.id)

    
    return artists_id

def get_artists_by_id(sp, artists_id):
    """ Get the artists from the artists_id with a spotipy request. """

    artists = []

    spotify_limit = 50
    # Since the limit of obtaining arists is 50, multiple requests have to be made.
    for i in range (ceil(len(artists_id)/spotify_limit)):

    # DEBUG
    # for i in range(1):

        artists_response = sp.artists(artists_id[i * spotify_limit: (i + 1) * spotify_limit])
        for artist in artists_response['artists']:
            artists.append(artist)

    return artists

def get_genres_from_artist(artist):
    """ Get all genres from the artist. """

    genres = []
    for genre in artist['genres']:
        if genre in popular_genres:
            genres.append(genre)

    return genres

def get_genre_count(sp, artists_count):
    """ Returns how many times an genre occurs in the usernames playlists. 
        Return:
            genre_count: dictionary, keys:genres, value:count
    """

    # Get the most populare genres
    # Since a song does not have a genre, the most popular genres get calculated from the most frequent artists and their genres:
    genre_count = {}

    artists_id = get_artists_id(artists_count)

    artists = get_artists_by_id(sp, artists_id)

    for artist in artists:
        genres = get_genres_from_artist(artist)
        for genre in genres:
            if genre in genre_count:
                genre_count[genre] += 1
            else:
                genre_count[genre] = 1

    return genre_count

def get_frequent_genres(genre_count, n):
    """ Get the nth most frequent genres. """

    sorted_genres = sorted(genre_count.items(), key=itemgetter(1), reverse=True)
    sorted_genres = dict(sorted_genres)

    return sorted_genres

def get_sp():

    # Not sure if this is needed for every request
    credentials = oauth2.SpotifyClientCredentials(
            client_id=get_env_var("CLIENT_ID"),
            client_secret=get_env_var("CLIENT_SECRET")
        )
    token = credentials.get_access_token()

    sp = spotipy.Spotify(auth=token)

    return sp

def get_total_dict_value(dictionary):
    """ Returns the sum of all values in a dictionary."""

    total = 0
    for value in dictionary.values():
        total += value

    return total

def get_sorted_in_common_artists(in_common_artists):
    """ Sort dictionary based on the third value. """
    sorted_artists = sorted(in_common_artists.items(), key=lambda e: e[1][2], reverse=True)
    sorted_artists = dict(sorted_artists)
    return sorted_artists

def get_all_songs_id_from_user(sp, username):
    """ Returns all public song ids from a user. """

    user_playlists = get_playlists(sp, username)

    songs = []
    for playlist in user_playlists:
        for song in get_songs(sp, username, playlist):
            
            songs.append(song['track']['id'])

    return songs

def get_auth_sp(user):
    """ Get an authorized spotipy object. """

    refresh_access_token(user)

    sp = spotipy.Spotify(auth=user.access_token)

    return sp

def create_playlist(sp, username1, username2 , in_common_songs):
    """ Creates an spotify playlist with all in_common_songs. This playlist is stored on the 
    account of username1. """
    
    playlist_name  = f"Music Match - {username2}"
    playlist = sp.user_playlist_create(username1, playlist_name, public = False)

    sp_limit = 100
    for i in range(ceil(len(in_common_songs)/100)):
        sp.user_playlist_add_tracks(username1, playlist['id'], in_common_songs[i * 100:(i + 1) * 100])

def refresh_access_token(user):
    """ Refreshes the access token for the user. """

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
    """ Checks if a user exists. Returns True if the user exists, else returns False."""

    try:
        sp.user(username)

        return True
    except:

        return False

def get_frequent_keys(dict1, dict2):
    """ 
    Returns a sorted list of keys based on the compared ranking between both artist_count.
    params:
        dict1, dict2: dictionary whose values have to be numbers
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
    """ Sort a dictionary based on the values from high to low. """

    return dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))


def get_n_dict_and_count(n, keys, user1_artist_count, user2_artist_count):
    """ Returns the first n artists, and their respective count for user1 and user2. """

    keys = keys[:n]
    user1_count, user2_count = [], []
    for key in keys:

        user1_count.append(user1_artist_count[key])
        user2_count.append(user2_artist_count[key])

    return keys, user1_count, user2_count

def get_genre_ranking(user1_genre_count, user1_total_genres, user2_genre_count, user2_total_genres):
    """ Returns a dictionary with the in common genres.
        key:genre_name, value:list [user1_count, user2_count, compared_ranking]
    """
    
    in_common_genres = {}

    for genre in user1_genre_count:
        if genre in user2_genre_count:
            temp1 = user1_genre_count[genre]
            temp2 = user2_genre_count[genre]
            in_common_genres[genre] = [
                temp1,
                temp2,
                (temp1 / user1_total_genres) * (temp2 / user2_total_genres)
            ]

    return get_sorted_in_common_artists(in_common_genres)

def write_data_to_db(username):
    """
    Writes the songs, artists and genres from username
    to the database.
    """

    sp = get_sp()

    userProfile =  UserProfile.objects.filter(username=username).first()
    if userProfile is None:
        userProfile = UserProfile(username=username)
        userProfile.save()


    # dict with arists who are not yet in the database
    # key: artist id, value: Artist object
    missing_artists_info = {}

    playlists = get_playlists(sp, username)
    for playlist in playlists:

        songs = get_songs(sp, username, playlist)

        for song in songs:
            
            song_id = song["track"]["id"]
            
            if Song.objects.filter(pk = song_id).exists():

                userProfile.songs.add(Song.objects.filter(pk = song_id).first())

                continue
  
            # Check if the song has a track attribute. 
            # I guess local songs dont have them, but are still obtained with the spotipy id. 
            if not song['track']:
                continue

            new_song = Song(id=song_id, name=song["track"]["name"])
            new_song.save()
            userProfile.songs.add(new_song)

            artists = []
            for artist in song["track"]["artists"]:

                artist_id = artist["id"]

                if artist_id is None:
                    continue
                
                artist_obj = Artist.objects.filter(pk = artist_id).first()
                
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

    return True

def add_missing_artists_info(sp, artists_dict):
    """ 
    Adds the genre information for new artists.
    sp: spotipy object
    artists_dict: dict, key = artist_id, value = Artist object
    """
    
    # Get all missing artists ids
    artists_id = list(artists_dict.keys())

    spotify_limit = 50
    artist_count = 0
    # Since the limit of obtaining arists is 50, multiple requests have to be made.
    for i in range (ceil(len(artists_id)/spotify_limit)):
        
        # Get json response for n artists
        # print(len(artists_id), i, artist_count)
        # print(artists_id[artist_count: artist_count + spotify_limit])
        artists_response = sp.artists(artists_id[artist_count: artist_count + spotify_limit])

        for artist in artists_response["artists"]:
            
            genres = []
            for genre in artist["genres"]:
                
                # Check if genre already exists
                genre_obj = Genre.objects.filter(pk = genre).first()
                if not genre_obj:

                    genre_obj = Genre(name = genre)
                    genre_obj.save()

                genres.append(genre_obj) 

            artist_obj = artists_dict[artists_id[artist_count]]
            artist_obj.genres.add(*genres)

            artist_count += 1
