"""
Set of functions related to the reading and writing of data from a spotify account.

"""

from math import ceil

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
