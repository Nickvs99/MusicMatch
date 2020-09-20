from django.urls import path
from . import views
from . import ajax

urlpatterns = [
    path("", views.home_view, name="index"),
    path("stats/", views.stats_view, name="stats"),
    path("compare/", views.compare_view, name="compare"),
    path("update/", views.update_view, name="update"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("verify/", views.verify, name="verify"),
    path("callback/", views.callback, name="callback"),
    path("forgot_password/", views.forgot_password_view, name="forgot_password"),
    path("account/", views.account_view, name="account"),
    path("account/reset_password", views.reset_password, name="reset_password"),
    path("account/<str:encr_message>/", views.account_message, name="account_message"),
    path("error/construction", views.construction, name="construction"),

    path("ajax/validate_username", ajax.validate_username, name="validate_username"),
    path("ajax/set_email", ajax.set_email),
    path("ajax/playlist", ajax.playlist, name="playlist"),
    path("ajax/stats", ajax.stats),
    path("ajax/compare", ajax.compare),
    path("ajax/validate_spotify_usernames", ajax.validate_spotify_usernames),
    path("ajax/validate_usernames", ajax.validate_usernames),
    path("ajax/check_access_token", ajax.check_access_token),
    path("ajax/update", ajax.update),
    path("ajax/check_update", ajax.check_update),

]