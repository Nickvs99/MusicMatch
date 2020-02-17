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

def get_artist_count(sp, username):
    """ Returns how many times an artist occurs in the usernames playlists. 
        Return:
            artist_count: dictionary, keys:artists, value:count
    """

    # Keeps track of how many times an artist/genre is featured in the public playlists
    artists_count = {}

    # Get all playlists
    for playlist in get_playlists(sp, username):

        songs = get_songs(sp, username, playlist)

        for song in songs:
            
            # Check if the song has a track attribute. 
            # I guess local songs dont have them, but are still obtained with the spotipy id. 
            if song['track']:
                artists = get_artists_from_song(song)
                for artist in artists:

                    artist_name = artist['name']
                    if artist_name in artists_count:
                        artists_count[artist_name].count += 1
                    else:
                        artists_count[artist_name] = Artist(artist_name, artist['id'])

    return artists_count

def get_frequent_artists(artists_count, n):
    """ Sorts the artists_count from high to low and return the nth most frequent artists. """
    
    # Sort dic from high to low, based on the count value from the Artists
    sorted_artists = sorted(artists_count.values(), key=attrgetter('count'), reverse=True)
    
    # Get the n most frequent artists. Store these in a dictionay, key: artist.name, value:artist.count. 
    frequent_artists = {}
    for artist in sorted_artists[:n]:
        frequent_artists[artist.name] = artist.count

    return frequent_artists

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

def get_total_artist_count(artist_count):
    """ Returns the total amount of artist mentions. """

    total_artists = 0
    for artist in artist_count:
        total_artists += artist_count[artist].count

    return total_artists

def get_sorted_in_common_artists(in_common_artists):
    """ Sort dictionary based on the third value. """
    sorted_artists = sorted(in_common_artists.items(), key=lambda e: e[1][2], reverse=True)
    sorted_artists = dict(sorted_artists)
    return sorted_artists

def get_total_genres(genre_count):
    """ Return the total number of genres."""
    
    total = 0
    for value in genre_count.values():
        total += value

    return total

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

def user_exists(request, sp, username):
    """ Checks if a user exists. Returns True if the user exists, else returns False."""

    try:
        sp.user(username)

        return True
    except:

        return False

def get_artist_ranking(user1_artist_count, user1_total_artists, user2_artist_count, user2_total_artists):
    """ Returns a dictionary with the in common artists.
        key:artist_name, value:list [user1_count, user2_count, compared_ranking]
    """

    in_common_artists = {}

    for artist in user1_artist_count:
        if artist in user2_artist_count:
            user1_count = user1_artist_count[artist].count
            user2_count = user2_artist_count[artist].count
            in_common_artists[artist] = [
                user1_count,
                user2_count,
                (user1_count / user1_total_artists) * (user2_count / user2_total_artists)
            ]

    # Returns sorted dictionary based on their compared ranking
    return get_sorted_in_common_artists(in_common_artists)

def get_n_artists_and_count(n, sorted_in_common_artists):
    """ Returns the first n artists, and their respective count for user1 and user2. """

    artists, user1_count, user2_count = [], [], []
    count = 0
    for key, value in sorted_in_common_artists.items():
        artists.append(key)
        user1_count.append(value[0])
        user2_count.append(value[1])
        if count == n:
            break
        count += 1

    return artists, user1_count, user2_count

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

    song_count = 0
    # Get all playlists
    for playlist in get_playlists(sp, username):


        songs = get_songs(sp, username, playlist)

        for song in songs:
            
            song_count += 1

            # if song_count == 10:
            #     return

            song_id = song["track"]["id"]

            if Song.objects.filter(pk = song_id).exists():
                continue
                
            # Check if the song has a track attribute. 
            # I guess local songs dont have them, but are still obtained with the spotipy id. 
            if not song['track']:
                continue
            
            artists_id = []
            for artist in song["track"]["artists"]:
                artists_id.append(artist["id"])

            artists = []
            for artist_id in artists_id:
                
                artist_obj = Artist.objects.filter(pk = artist_id).first()
                if artist_obj:

                    artists.append(artist_obj)                    
                    continue
                
                sp_artist = sp.artists([artist_id])

                print(sp_artist)
                genres = []
                for genre in sp_artist["artists"][0]["genres"]:
                    
                    genre_obj = Genre.objects.filter(pk = genre).first()

                    if not genre_obj:
                        genre_obj = Genre(name = genre)
                        genre_obj.save()

                    genres.append(genre_obj)       
                    
                artist_obj = Artist(id=artist_id, name=sp_artist["artists"][0]["name"])
                artist_obj.save()

                artist_obj.genres.add(*genres)

                artists.append(artist_obj)

            new_song = Song(id=song_id, name=song["track"]["name"])
            new_song.save()
            new_song.artists.add(*artists)

    return artists_count