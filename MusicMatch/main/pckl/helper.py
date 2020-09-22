"""
Set of functions used for pickling(?) files.
"""

import pickle

from main.util.util import remove_chars

def get_user_file_path(username):
    """
    Returns the path to a spotify_users file
    Args:
        username: str
    Returns:
        path: str
    """

    string = remove_chars(username)
    return f"file_storage/spotify_users/{string}.pickle"

def get_artist_file_path(artist):
    """
    Returns the path to a artist file
    Args:
        artist: str
    Returns:
        path: str
    """

    string = remove_chars(artist)
    return f"file_storage/artists/{string}.pickle"

def get_pickle_data(path):
    """
    Returns the data stored in a pckl file
    Args:
        path: str
    Returns:
        data stored in the pckl file
    """
    f = open(path, "rb")

    data = pickle.load(f)

    f.close()

    return data

def write_pickle_data(path, data):
    """
    Writes the data to a pckl file
    Args:
        path: str
        data: anything
    """
    f = open(path, "wb+")

    pickle.dump(data, f)

    f.close()
