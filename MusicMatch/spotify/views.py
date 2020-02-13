from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

from .func import *

def stats(request):

    return render(request, "spotify/stats.html")

def get_stats(request):

    username = json.loads(request.body).get('username', None)

    sp = get_sp()

    if not user_exists(request,sp, username):
        data = {
            "usernameValid": False
        }
        return JsonResponse(data)


    artists_count = get_artist_count(sp, username)

    frequent_artists = get_frequent_artists(artists_count, 10)
    
    genre_count = get_genre_count(sp, artists_count)

    frequent_genres = get_frequent_genres(genre_count, 100)

    if artists_count == {}:
        messages.warning(request, f"No songs found for {username}. Make sure the playlists are set to public.")
    
    data = {
        "usernameValid": True,
        "artist_count": frequent_artists,
        "genre_count": frequent_genres,
    }

    return JsonResponse(data)

def compare(request):

    return render(request, "spotify/compare.html")

def get_comparison(request):
    """ Get the comparison between two usernames. """

    jsonLoad = json.loads(request.body)

    username1 = jsonLoad["username1"]
    username2 = jsonLoad["username2"]

    data = {
        "username1Valid": True,
        "username2Valid": True
    }

    sp = get_sp()

    # Check if both usernames are valid
    if not user_exists(request, sp, username1):

        data["username1Valid"] = False
    
    if not user_exists(request, sp, username2):

        data["username2Valid"] = False  

    if not data["username1Valid"] or not data["username2Valid"]:

        return JsonResponse(data)

    user1_artist_count = get_artist_count(sp, username1)
    user2_artist_count = get_artist_count(sp, username2)

    user1_total_artists = get_total_artist_count(user1_artist_count)
    user2_total_artists = get_total_artist_count(user2_artist_count)

    sorted_in_common_artists = get_artist_ranking(user1_artist_count, user1_total_artists, user2_artist_count, user2_total_artists)

    artists, user1_count, user2_count = get_n_artists_and_count(10, sorted_in_common_artists)

    user1_genre_count = get_genre_count(sp, user1_artist_count)
    user2_genre_count = get_genre_count(sp, user2_artist_count)

    user1_total_genres = get_total_genres(user1_genre_count)
    user2_total_genres = get_total_genres(user2_genre_count)

    sorted_in_common_genres = get_genre_ranking(user1_genre_count, user1_total_genres, user2_genre_count, user2_total_genres)

    genres, user1_genre_count, user2_genre_count = get_n_artists_and_count(10, sorted_in_common_genres)

    # Set data in dict 
    data["artists"] = artists
    data["user1_artist_count"] = user1_count
    data["user2_artist_count"] = user2_count

    data["genres"] = genres
    data["user1_genre_count"] = user1_genre_count
    data["user2_genre_count"] = user2_genre_count

    return JsonResponse(data)

def playlist(request):
    """ Creates a playlist for username with all the songs both users have in their playlist."""

    jsonLoad = json.loads(request.body)

    username1 = jsonLoad["username1"]
    username2 = jsonLoad["username2"]

    data = {
        "username1Valid": True,
        "username2Valid": True,
    }

    sp = get_sp()

    # Check if both usernames are valid
    if not user_exists(request, sp, username1):

        data["username1Valid"] = False
    
    if not user_exists(request, sp, username2):

        data["username2Valid"] = False  

    if not data["username1Valid"] or not data["username2Valid"]:

        return JsonResponse(data)

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
