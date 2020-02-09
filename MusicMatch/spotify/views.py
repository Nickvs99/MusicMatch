from django.shortcuts import render, redirect
from django.contrib import messages

from .func import *

def stats(request, username):
    """ Retrieves public information about the username's spotify account."""

    sp = get_sp()

    if not user_exists(request,sp, username):
        return render(request, "spotify/stats.html")

    artists_count = get_artist_count(sp, username)

    frequent_artists = get_frequent_artists(artists_count, 10)
    
    genre_count = get_genre_count(sp, artists_count)

    frequent_genres = get_frequent_genres(genre_count, 100)

    if artists_count == {}:
        messages.warning(request, f"No songs found for {username}. Make sure the playlists are set to public.")
    
    context = {
        "username": username,
        "artist_count": frequent_artists,
        "genre_count": frequent_genres,
    }

    return render(request, "spotify/stats.html", context=context)

def compare(request, username1, username2):
    """ Compares the music taste between two users. """

    # Only show two search fields when both users are 'None'. This happens when navigated from the navbar.
    if username1 == 'None' and username2 == 'None':

        return render(request, "spotify/compare.html")

    sp = get_sp()

    if not user_exists(request, sp, username1) or not user_exists(request, sp, username2):

        return render(request, "spotify/compare.html")

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

    # Add message when username1 and username2 have nothing in common
    if len(artists) == 0:
        messages.warning(request, f"{username1} and {username2} have no artists in common.")
    
    if len(genres) == 0:
        messages.warning(request, f"{username1} and {username2} have no genres in common.")
    
    context = {
        "artists": artists,
        "user1_artist_count": user1_count,
        "user2_artist_count": user2_count,

        "genres": genres,
        "user1_genre_count": user1_genre_count,
        "user2_genre_count": user2_genre_count,

        "username1": username1,
        "username2": username2,
    }
    return render(request, "spotify/compare.html", context)

def playlist(request, username1, username2):
    """ Creates a playlist for username with all the songs both users have in their playlist."""

    user = User.objects.get(username=username1)
    user = UserProfile.objects.get(user=user)

    if not user.access_token:
        return redirect("verify")

    sp = get_auth_sp(user)

    user1_songs = get_all_songs_id_from_user(sp, username1)
    user2_songs = get_all_songs_id_from_user(sp, username2)

    in_common_songs = []
    for song in user2_songs:
        if song in user1_songs:
            in_common_songs.append(song)

    create_playlist(sp, username1, username2, in_common_songs)

    messages.success(request, "Succes! Check your spotify account for your newly created playlist!")
    
    return redirect("compare", username1, username2)

def stats_redirect(request):
    """ 
        This view redirect to the stats page. It is triggered when a user does a 
        POST request on stats.html. 
    """

    if request.method == "POST":
        username = request.POST["username"]

        if not username:
            return redirect("stats", request.user)

        return redirect("stats", username)

    elif request.method == "GET":

        return redirect("stats", request.user)

def compare_redirect(request):
    """ 
        This view redirect to the compare page. It is triggered when a user does a 
        POST request on compare.html. 
    """

    if request.method == "POST":

        username1 = request.POST["username1"]
        username2 = request.POST["username2"]

        if not username1 or not username2:
            messages.error(request, "Both fields are required.")
            return redirect("compare", "None", "None")

        return redirect("compare", username1, username2)

    elif request.method == "GET":

        messages.error(request, "Both field need to be filled in.")

        return redirect("compare", "None", "None")
    
