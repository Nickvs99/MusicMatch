from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

import os
import requests
import json

from main.email import send_email
from main.fernet import decrypt_message, encrypt_message
from main.models import ExtendedUser
from main.spotify.auth import get_auth_sp
from main.util.util import get_env_var

def stats_view(request):

    return render(request, "main/legacy/stats.html")

def compare_view(request):

    return render(request, "main/legacy/compare.html")

def update_view(request):

    return render(request, "main/pages/update.html")

def home_view(request):
    """ Homepage view """

    return render(request, "main/pages/index.html")

def login_view(request):
    """ Login view. Manages the login process. """

    if request.method == 'GET':

        # TODO auto expand login form
        return redirect("index")
    
    elif request.method =='POST':

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in.")

            # Check if the user already has an access token.
            user = ExtendedUser.objects.get(user__username=username)
            if user.access_token:
                return redirect("index")

            return redirect("verify")

        else:
            messages.error(request, "Invalid credentials.")

            # TODO auto collapse login form
            return redirect("index")

def logout_view(request):
    """ Logs the user out. Then redirects to the login view."""

    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out.")

    else:
        messages.warning(request,"You are already logged out.")

    return redirect("index")

def register_view(request):
    """ Register view. Has the field to register a user."""

    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'Please logout before registering a new user')
            return redirect("index")

        return render(request, "main/pages/register.html")

    elif request.method == 'POST':

        # Get field from form
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        # Check if all fields are filled in
        if not (username and password and email):
            messages.error(request, "All fields are required")
            return render(request, "main/pages/register.html")

        # Check if username is already taken
        user = User.objects.filter(username=username)
        if user:
            messages.error(request, "Username already taken.")
            return render(request, "main/pages/register.html")

        user = User.objects.create_user(username, email, password)
        user.save()

        # Save it to the extended User model
        ExtendedUser(user=user).save()
        
        messages.success(request, "Successfully registered.")

        link = get_env_var("DOMAIN") + "/account/" + encrypt_message(f"remove_email/{username}")
        message = f'Hey {username}, \n\nThank you for signing up with Spotifyfy! \n\n If this is not you, please click on the following link. This link will remove your email adres.\n {link}'
        send_email('Spotifyfy - confirmation email', message, [email], request=request)
              
        login(request, user)
        return redirect("index")

def account_view(request):
    """ 
    Account view. View info about the authenticated profile and let the user edit its 
    email, spotify_account and password.
    """

    if not request.user.is_authenticated:
        messages.warning(request,  "You have to be logged in to see this page")
        # TODO auto collapse login form
        return redirect("index")

    user = ExtendedUser.objects.filter(user=request.user).first()

    context = {
        "user": user,
        "username": user.user.username,
        "email": user.user.email,
        "spotify_account": user.spotify_account,
    }

    return render(request, "main/pages/account.html", context)

def forgot_password_view(request):
    """ Lets the user change its password when it has forgotten his. """

    if request.method == "GET":
        return render(request, "main/pages/forgot_password.html")

    elif request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]

        # Check if the combination exists
        if not User.objects .filter(username=username, email=email).exists():
            messages.error(request, "The username - email combination does not exist.")
            return render(request, "main/pages/forgot_password.html")
        
        link = get_env_var("DOMAIN") + "/account/" + encrypt_message(f"change_password/{username}")
        message = f"Hey {username} \n\n. Please click on the following link to reset your password: \n\n {link}"
        success = send_email("Spotifyfy - Change of password", message, email, request=request)

        if success:
            messages.success(request, "Check your email!")
            
        return render(request, "main/pages/forgot_password.html")

def verify(request):
    """ 
    Get authorized token,  authorization-code-flow Step 1.
    https://developer.spotify.com/documentation/general/guides/authorization-guide/
    """

    API_BASE = 'https://accounts.spotify.com'
    CLI_ID = get_env_var("CLIENT_ID")
    REDIRECT_URI = f"{get_env_var('DOMAIN')}/callback/"
    SCOPE = "playlist-modify-private"
    SHOW_DIALOG = True
    auth_url = f'{API_BASE}/authorize?client_id={CLI_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}&show_dialog={SHOW_DIALOG}'

    return redirect(auth_url)

def callback(request):
    """
    authorization-code-flow Step 2.
    Get the refresh and access tokens.
    https://developer.spotify.com/documentation/general/guides/authorization-guide/

    Link spotify account to current authenticated account.
    """

    code = request.GET.get('code')

    # Get initial access token and refresh token
    API_BASE = 'https://accounts.spotify.com'
    auth_token_url = f"{API_BASE}/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        "redirect_uri":f"{get_env_var('DOMAIN')}/callback/",
        "client_id":get_env_var("CLIENT_ID"),
        "client_secret":get_env_var("CLIENT_SECRET")
        })

    res_body = res.json()

    access_token =  res_body.get("access_token")
    refresh_token = res_body.get("refresh_token")

    if not access_token:
        messages.warning(request, "Some features will not work since you rejected access." )
        return redirect("index")

    # Save the tokens to the extended user
    user = ExtendedUser.objects.get(user__username=request.user)
    user.access_token = access_token
    user.refresh_token = refresh_token
    user.save()

    # Get the profiles id and link it to the extended user
    sp = get_auth_sp(user)
    response = sp.current_user()
    
    messages.success(request, "Your spotify account is now tied to your Spotifyfy account. ")
    user.spotify_account = response["id"]
    user.save()

    return redirect("index")

def account_message(request, encr_message):
    """ 
    Performs an action based on the encrypted message in the url.
    Args:
        message: str, encrypted message
    """

    message = decrypt_message(encr_message)

    # Gets the action and username from the message
    index = message.find("/")
    action = message[:index]
    username = message[index + 1:]

    if action == "remove_email":

        user = User.objects.filter(username=username).first()
        
        if user is None:
            messages.info(request, "The account associated with your email no longer exists.")
        else:
            user.email = ""
            user.save()

            messages.success(request, "Your email has been succesfully removed.")

    elif action == "change_password":

        context = {
            "username": username,
            "message": encr_message
        }

        if request.method == "GET":

            return render(request, "main/pages/change_password.html", context)

        elif request.method == "POST":
            
            new_password = request.POST["newPassword"]
            confirm_password = request.POST["confirmPassword"]

            if new_password != confirm_password:
                
                messages.error(request, "The passwords are not the same")

                return render(request, "main/pages/change_password.html", context)

            user = User.objects.filter(username=username).first()

            user.set_password(new_password)
            user.save()

            messages.success(request, "Successfully changed password.")

            return redirect("index")
    else:
        messages.error(request, "Something went wrong on our end. Sorry for the inconvenience.")

    return redirect("index")

def reset_password(request):
    """ Resets the password of the currently loggedin user. """

    if request.method == "get":
        messages.error(request, "Invalid request")
        return redirect("index")
    
    # Get field from form
    old_password = request.POST["oldPassword"]
    new_password = request.POST["newPassword"]
    confirm_password = request.POST["confirmPassword"]

    user = request.user
    
    if not user.check_password(old_password):
        messages.error(request, "Invalid password")
        return redirect("account")

    if new_password != confirm_password:
        messages.error(request, "Confirm password is not equal to the new password.")
        return redirect("account")
    
    user.set_password(new_password)
    user.save()

    # Set password logs the user out. With this step is user is re-authenticated.
    update_session_auth_hash(request, request.user)

    messages.success(request, "Succesfully changed password")

    return redirect("account")

def construction(request):

    return render(request, "main/pages/construction.html")