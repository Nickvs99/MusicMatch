from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import UserProfile

import os
import requests
import json

from utils.utils import get_env_var

def index(request):
    """ Homepage view """

    return render(request, "Authentication/index.html")

def login_view(request):
    """ Login view """

    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, "You are already logged in.")

            return redirect("index")

        return render(request, "Authentication/login.html")
    
    elif request.method =='POST':

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in.")

            # Check if the user already has an access token.
            user = UserProfile.objects.get(user=request.user)
            if user.access_token:
                return redirect("index")

            return redirect("verify")

        else:
            messages.error(request, "Invalid credentials.")
            return render(request, "Authentication/login.html")

def logout_view(request):
    """ The user is now logged out. """

    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out.")

    else:
        messages.warning(request,"You are already logged out.")

    return redirect("login")

def register(request):
    """ Register view. Has the field to register a user. """

    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You have to logout, to register a new user.')
            return redirect("index")

        return render(request, "Authentication/register.html")

    elif request.method == 'POST':

        # Get field from form
        username = request.POST["username"]
        password = request.POST["password"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]

        # Check if all fields are filled in
        if not (username and password and firstname and lastname and email):
            messages.error(request, "All fields are required")
            return render(request, "Authentication/register.html")

        # Check if username is already taken
        user = User.objects.filter(username=username)
        if user:
            messages.error(request, "Username already taken.")
            return render(request, "Authentication/register.html")

        user = User.objects.create_user(username, email, password, first_name=firstname, last_name = lastname)
        user.save()

        # Save it to the extended User model
        user = UserProfile(user=user)
        user.save()
        
        messages.success(request, "Successfully registered.")

        return redirect("login")

def validate_username(request):

    username = json.loads(request.body).get('username', None)

    data = {
        'usernameTaken': User.objects.filter(username=username).exists(),
    }

    return JsonResponse(data)

def verify(request):
    """ 
    Get authorized token,  authorization-code-flow Step 1.
    https://developer.spotify.com/documentation/general/guides/authorization-guide/
    """

    API_BASE = 'https://accounts.spotify.com'
    CLI_ID = get_env_var("CLIENT_ID")
    REDIRECT_URI = get_env_var("REDIRECT_URI")
    SCOPE = "playlist-modify-private"
    SHOW_DIALOG = True
    auth_url = f'{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'
    print(auth_url)
    return redirect(auth_url)

def callback(request):
    """
    authorization-code-flow Step 2.
    Get the refresh and access tokens.
    https://developer.spotify.com/documentation/general/guides/authorization-guide/
    """

    code = request.GET.get('code')

    # Get initial access token and refresh token
    API_BASE = 'https://accounts.spotify.com'
    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":"http://127.0.0.1:8000/callback/",
        "client_id":get_env_var("CLIENT_ID"),
        "client_secret":get_env_var("CLIENT_SECRET")
        })

    res_body = res.json()

    access_token =  res_body.get("access_token")
    refresh_token = res_body.get("refresh_token")

    if not access_token:
        messages.warning(request, "Some features will not work since you rejected access." )
        return redirect("index")

    user = UserProfile.objects.get(user=request.user)
    user.access_token = access_token
    user.refresh_token = refresh_token
    user.save()

    return redirect("index")