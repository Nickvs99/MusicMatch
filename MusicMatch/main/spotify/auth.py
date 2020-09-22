"""
Set of functions related to authorisation with the spotify api.

"""

import requests

import spotipy
import spotipy.oauth2 as oauth2

from main.util.util import get_env_var

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

    return spotipy.Spotify(auth=token)

def get_auth_sp(user):
    """
    Get an authorized spotipy object for the user.
    Args:
        user: ExtendedUser object
    Returns:
        authorized spotipy object
    """

    refresh_access_token(user)

    return spotipy.Spotify(auth=user.access_token)

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
