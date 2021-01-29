import datetime
import json
import os

from django.contrib.auth.models import User

from main.email import send_email
from main.fernet import encrypt_message
from main.models import ExtendedUser
import main.pckl.helper as pckl_helper
from main.server_data import write_data_to_server
from main.spotify.auth import get_auth_sp, get_sp, user_exists
from main.spotify.data import create_playlist
from main.util.dict import get_dict_comparison, get_shared_keys, get_unique_keys 
from main.util.lst import get_shared_items, get_unique_items
from main.util.util import get_env_var, JsonResponseWrapper


def stats(request):
    """
    Returns the stats for a user. This user has to be an entry in the SpotifyUser table.
    Returns:
        artist_count: dict, key: artist name (str), value: count (int)
        genre_count: dict, key: genre name (str), value: count (int)
        total_songs: int, Total number of songs
        total_artists: int, Total number of artists
        total_genres: int, Total number of genres
    """

    username = json.loads(request.body).get('username', None)

    path = pckl_helper.get_user_file_path(username)
    user = pckl_helper.get_pickle_data(path)

    user.songs_check(request)

    data = {
        "artist_count": user.artist_count,
        "genre_count": user.genre_count,
        "total_songs": len(user.song_ids),
        "total_artists": len(user.artist_count),
        "total_genres": len(user.genre_count),
    }

    return JsonResponseWrapper(request, data)

def compare(request):
    """
    Returns the data used for the comparison between two users.
    Both users have to be an entry in the SpotifyUser table.
    Returns:
        unique_songs: int, The number of unique songs accross the songs of both users
        unique_artists: int, idem but for artists
        unique_genres: int, idem but for genres
        
        shared_songs: int, The number of songs shared between the two users
        shared_artists: int, idem but for artists
        shared_genres: int, idem but for genres

        artist_comparison: list[artist_name (str), list[float, float]], sorted decreasingly
        genre_comparison: list[genre_name (str), list[float, float]], sorted decreasingly
    """

    jsonLoad = json.loads(request.body)

    usernames = jsonLoad["usernames"]

    path1 = pckl_helper.get_user_file_path(usernames[0])
    user1 = pckl_helper.get_pickle_data(path1)

    path2 = pckl_helper.get_user_file_path(usernames[1])
    user2 = pckl_helper.get_pickle_data(path2)

    user1.songs_check(request)
    user2.songs_check(request)

    artist_comparison = get_dict_comparison(user1.artist_count, user2.artist_count)

    genre_comparison = get_dict_comparison(user1.genre_count, user2.genre_count)

    data = {
        "unique_songs": len(get_unique_items(user1.song_ids, user2.song_ids)),
        "shared_songs": len(get_shared_items(user1.song_ids, user2.song_ids)),
        
        "unique_artists": get_unique_keys(user1.artist_count, user2.artist_count),
        "shared_artists": get_shared_keys(user1.artist_count, user2.artist_count),
        
        "unique_genres": get_unique_keys(user1.genre_count, user2.genre_count),
        "shared_genres": get_shared_keys(user1.genre_count, user2.genre_count),

        "artist_comparison": artist_comparison,
        "genre_comparison": genre_comparison,
    }

    return JsonResponseWrapper(request, data)

def playlist(request):
    """
    Creates a playlist for the logged in user with songs based on the username input.
    """

    jsonLoad = json.loads(request.body)

    usernames = jsonLoad["usernames"]

    user = ExtendedUser.objects.get(user__username=request.user.username)

    path1 = pckl_helper.get_user_file_path(usernames[0])
    user1 = pckl_helper.get_pickle_data(path1)

    path2 = pckl_helper.get_user_file_path(usernames[1])
    user2 = pckl_helper.get_pickle_data(path2)

    sp = get_auth_sp(user)

    in_common_songs = get_shared_items(user1.song_ids, user2.song_ids)

    # Create a playlist for the spotify account of the user
    create_playlist(sp, user.spotify_account, usernames, list(in_common_songs))
    
    data = {}
    return JsonResponseWrapper(request, data)

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

    return JsonResponseWrapper(request, data)

def validate_usernames(request):
    """
    Checks whether the usernames are found in the file_storage/spotify_users.
    Returns:
        usernames dict{str: bool} username: bool, True if the username has a cached version.
    """
    jsonLoad = json.loads(request.body)

    usernames = jsonLoad["usernames"]

    data = {}

    for username in usernames:
        
        path = pckl_helper.get_user_file_path(username)
        data[username] = os.path.isfile(path)

    return JsonResponseWrapper(request, data)

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

        return JsonResponseWrapper(request, data)

    user = ExtendedUser.objects.filter(user__username=request.user.username).first()

    if user.access_token == "":
        data["access_token"] = False
        return JsonResponseWrapper(request, data)

    return JsonResponseWrapper(request, data)

def update(request):
    """
    Updates a user. 
    If the user does not exist, create an entry in the SpotifyUser table.
    """
    jsonLoad = json.loads(request.body)

    username = jsonLoad["username"]

    write_data_to_server(username)
    
    data = {}
    return JsonResponseWrapper(request, data)

def check_update(request):
    """ 
    Checks wheter a user has to be updated.
    Returns:
        update: bool, True when user does not exist or 
            if it has been more than 14 days since the last update.
    """
    data = {"update": True}

    jsonLoad = json.loads(request.body)

    username = jsonLoad["username"]

    path = pckl_helper.get_user_file_path(username)
    if not os.path.isfile(path):

        return JsonResponseWrapper(request, data)

    user = pckl_helper.get_pickle_data(path)

    if user.last_updated is None:

        return JsonResponseWrapper(request, data)

    # Check if it has been more than x days since last update
    delta = datetime.date.today() - user.last_updated
    if delta.days > 14:
        
        return JsonResponseWrapper(request, data)

    data["update"] = False

    return JsonResponseWrapper(request, data)    

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

    return JsonResponseWrapper(request, data)

def set_email(request):
    """ Change the email of the currently authenticated user. """

    jsonLoad = json.loads(request.body)

    email = jsonLoad["email"]

    user = User.objects.filter(username=request.user.username).first()

    user.email = email
    user.save()

    link = get_env_var("DOMAIN") + "/account/" + encrypt_message(f"remove_email/{request.user.username}")
    message = f"Hey {request.user.username}\n\nYour email has successfully changed. If this is not you, please click on the following link. This link will remove your email adres.\n {link}"
    send_email("Spotifyfy - Change of email", message, [email], request=request)

    data = {}
    return JsonResponseWrapper(request, data)
