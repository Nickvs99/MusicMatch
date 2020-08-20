from django.http import JsonResponse
from django.db import transaction
from django.contrib.auth.models import User

import datetime
import json

from .func import *

def stats(request):
    """
    Returns the stats for a user. This user has to be an entry in the SpotifyUser table.
    Returns:
        artist_count: dict, key: artist name (str), value: count (int)
        genre_count: dict, key: genre name (str), value: count (int)
    """

    username = json.loads(request.body).get('username', None)

    user = SpotifyUser.objects.filter(pk=username).first()

    total_artists = get_total_artists(user)

    total_songs = get_total_songs(user)

    total_genres = get_total_genres(user)

    frequent_artists = get_n_heighest_from_dict(user.artist_count, 10)
    
    frequent_genres = get_n_heighest_from_dict(user.genre_count, 15)

    data = {
        "artist_count": frequent_artists,
        "genre_count": frequent_genres,
        "total_songs": total_songs,
        "total_artists": total_artists,
        "total_genres": total_genres,
    }

    return JsonResponse(data)

def compare(request):
    """
    Returns the data used for the comparison between two users.
    Both users have to be an entry in the SpotifyUser table.
    Returns:
        artists: list (str) artist names 
        user1_artist_count: dict, keys: artist name (str), value: count (int)
        user2_artist_count: dict, keys: artist name (str), value: count (int)

        genres: list (str) genre names 
        user1_genre_count: dict, keys: artist name (str), value: count (int)
        user2_genre_count: dict, keys: artist name (str), value: count (int)
    """

    jsonLoad = json.loads(request.body)

    usernames = jsonLoad["usernames"]

    user1 = SpotifyUser.objects.filter(pk=usernames[0]).first()
    user2 = SpotifyUser.objects.filter(pk=usernames[1]).first()

    user1_artist_count = user1.artist_count
    user1_genre_count = user1.genre_count

    user2_artist_count = user2.artist_count
    user2_genre_count = user2.genre_count

    artist_comparison = get_dict_comparison(user1_artist_count, user2_artist_count)

    genre_comparison = get_dict_comparison(user1_genre_count, user2_genre_count)

    data = {
        "artist_comparison": artist_comparison,
        "genre_comparison": genre_comparison,

    }
    

    return JsonResponse(data)

def playlist(request):
    """
    Creates a playlist for the logged in user with songs based on the username input.
    """

    jsonLoad = json.loads(request.body)

    usernames = jsonLoad["usernames"]

    user = ExtendedUser.objects.get(user__username=request.user.username)

    user1 = SpotifyUser.objects.get(pk=usernames[0])
    user2 = SpotifyUser.objects.get(pk=usernames[1])

    sp = get_auth_sp(user)

    user1_songs = user1.songs.all()
    user2_songs = user2.songs.all()

    in_common_songs = []
    for song in user2_songs:
        if song in user1_songs:
            in_common_songs.append(song.id)

    create_playlist(sp, user.user.username, usernames, in_common_songs)
    
    data = {}
    return JsonResponse(data)

def validate_spotify_usernames(request):
    """
    Checks whether the usernames have a spotify account.
    Returns:
        usernames username: bool, True if the username has a spotify account
        all_valid: bool, True when all usernames are valid
    """
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
    """
    Checks whether the usernames have an enrie in the SpotifyUser table.
    Returns:
        usernames username: bool, True if the username has a spotify account
        all_valid: bool, True when all usernames are valid
    """
    jsonLoad = json.loads(request.body)

    usernames = jsonLoad["usernames"]

    sp = get_sp()

    data = {}

    all_valid = True
    for username in usernames:
        
        if not SpotifyUser.objects.filter(pk=username).exists():

            data[username] = False
            all_valid = False

        else:
            data[username] = True

    return JsonResponse(data)

def check_access_token(request):
    """
    Checks wheter a user has an access token.
    Returns:
        loggedin: bool, True when the user is logged in
        access_token: bool, True when the user has an access token
    """

    data = {
        "loggedin": True,
        "access_token": True,
    }

    if not request.user.is_authenticated:
        data["loggedin"] = False

        return JsonResponse(data)

    user = ExtendedUser.objects.filter(user__username=request.user.username).first()

    if user.access_token == "":
        data["access_token"] = False
        return JsonResponse(data)

    return JsonResponse(data)

@transaction.atomic
def update(request):
    """
    Updates a user. 
    If the user does not exist, create an entry in the SpotifyUser table.
    """
    jsonLoad = json.loads(request.body)

    username = jsonLoad["username"]

    user = SpotifyUser.objects.filter(pk=username).first()

    if user is None:
        user = SpotifyUser(username=username)
        user.save()

    # Clear all song relationships with this user
    if user.songs:
        user.songs.clear()

    write_data_to_db(username)

    data = {}
    return JsonResponse(data)

def check_update(request):
    """ 
    Checks wheter a user has to be updated.
    Returns:
        update: bool, True when user does not exist or 
            if it has been more than 14 days since the last update.
    """
    data = {}

    jsonLoad = json.loads(request.body)

    username = jsonLoad["username"]

    user =  SpotifyUser.objects.filter(username=username).first()
    if user is None:

        data["update"] = True

        return JsonResponse(data)

    if user.last_updated is None:
        data["update"] = True

        return JsonResponse(data)

    # Check if it has been more than x days since last update
    delta = datetime.date.today() - user.last_updated
    if delta.days > 14:
        
        data["update"] = True

        return JsonResponse(data)

    data["update"] = False

    return JsonResponse(data)

def cache_results(request):
    """
    Caches the results for a user. These results are
    artist_count and genre_count.
    """

    jsonLoad = json.loads(request.body)

    username = jsonLoad["username"]

    user = SpotifyUser.objects.filter(username=username).first()
    
    results = get_data(user)

    user.artist_count = results[0]
    user.genre_count = results[1]

    user.save()

    data = {}
    return JsonResponse(data)

def validate_username(request):
    """
    Checks if a username is already taken or not. 
    Returns:
        dict:
            "valid_username": bool
    """

    username = json.loads(request.body).get('username', None)

    data = {
        'valid_username': not User.objects.filter(username=username).exists(),
    }

    return JsonResponse(data)

def set_email(request):
    """ Change the email of the currently authenticated user. """

    jsonLoad = json.loads(request.body)

    email = jsonLoad["email"]

    user = User.objects.filter(username=request.user.username).first()

    user.email = email
    user.save()

    link = get_env_var("DOMAIN") + "/account/" + encrypt_message(f"remove_email/{request.user.username}")
    message = f"Hey {request.user.username}\n\nYour email has successfully changed. If this is not you, please click on the following link. This link will remove your email adres.\n {link}"
    send_email("MusicMatch - Change of email", message, [email])

    data = {}
    return JsonResponse(data)
