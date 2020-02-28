from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db import transaction

from Authentication.models import UserProfile

from .func import *

def stats(request):

    return render(request, "spotify/stats.html")

def get_stats(request):

    # TODO different syntax
    username = json.loads(request.body).get('username', None)

    user_profile = UserProfile.objects.filter(pk=username).first()

    artist_count, genre_count = get_artist_count(user_profile)

    frequent_artists = get_n_heighest_from_dict(artist_count, 10)
    
    frequent_genres = get_n_heighest_from_dict(genre_count, 15)

    data = {
        "artist_count": frequent_artists,
        "genre_count": frequent_genres,
    }

    return JsonResponse(data)

def compare(request):

    return render(request, "spotify/compare.html")

def get_comparison(request):
    """ Get the comparison between two usernames. """

    jsonLoad = json.loads(request.body)

    usernames = jsonLoad["usernames"]

    user1 = UserProfile.objects.filter(pk=usernames[0]).first()
    user2 = UserProfile.objects.filter(pk=usernames[1]).first()

    user1_artist_count, user1_genre_count = get_artist_count(user1)
    user2_artist_count, user2_genre_count = get_artist_count(user2)

    artists_sorted_all = get_frequent_keys(user1_artist_count, user2_artist_count)

    artists, user1_artist_count, user2_artist_count = get_n_dict_and_count(10, artists_sorted_all, user1_artist_count, user2_artist_count)

    genres_sorted_all = get_frequent_keys(user1_genre_count, user2_genre_count)

    genres, user1_genre_count, user2_genre_count = get_n_dict_and_count(10, genres_sorted_all, user1_genre_count, user2_genre_count)

    data = {}
    
    # Set data in dict 
    data["artists"] = artists
    data["user1_artist_count"] = user1_artist_count
    data["user2_artist_count"] = user2_artist_count

    data["genres"] = genres
    data["user1_genre_count"] = user1_genre_count
    data["user2_genre_count"] = user2_genre_count

    return JsonResponse(data)

def playlist(request):
    """ Creates a playlist for username with all the songs both users have in their playlist."""

    jsonLoad = json.loads(request.body)

    username1 = jsonLoad["username1"]
    username2 = jsonLoad["username2"]

    data = {}
    
    # Check if user is logged in
    if not request.user.is_authenticated:
        data["error"] = "You have to be logged in to create a playlist."

        return JsonResponse(data)

    # If both valid get the authorised spotipy object
    user = User.objects.get(username=request.user)
    user = UserProfile.objects.get(user=user)

    if not user.access_token:
        
        data["error"] = "This profile does not contain an access_token."
        return JsonResponse(data)


    sp = get_auth_sp(user)

    user1_songs = get_all_songs_id_from_user(sp, username1)
    user2_songs = get_all_songs_id_from_user(sp, username2)

    in_common_songs = []
    for song in user2_songs:
        if song in user1_songs:
            in_common_songs.append(song)

    create_playlist(sp, username1, username2, in_common_songs)
    
    return JsonResponse(data)

def validate_spotify_usernames(request):

    jsonLoad = json.loads(request.body)

    usernames = jsonLoad["usernames"]

    sp = get_sp()

    data = {}
    data["usernames"] = {}

    all_valid = True
    for username in usernames:
        if not user_exists(sp, username):

            data["usernames"][username] = False
            all_valid = False

        else:
            data["usernames"][username] = True

    data["all_valid"] = all_valid

    return JsonResponse(data)

def validate_usernames(request):
    
    jsonLoad = json.loads(request.body)

    usernames = jsonLoad["usernames"]

    sp = get_sp()

    data = {}

    all_valid = True
    for username in usernames:
        
        if not UserProfile.objects.filter(pk=username).exists():

            data[username] = False
            all_valid = False

        else:
            data[username] = True

    return JsonResponse(data)
    
@transaction.atomic
def write_data(request):

    jsonLoad = json.loads(request.body)

    username = jsonLoad["username"]

    write_data_to_db(username)

    data = {}
    return JsonResponse(data)
    