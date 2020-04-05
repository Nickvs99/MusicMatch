from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.stats_view, name="stats"),
    path("compare/", views.compare_view, name="compare"),
    path("update/", views.update_view, name="update"),
    path("ajax/playlist", views.playlist, name="playlist"),
    path("ajax/stats", views.stats),
    path("ajax/compare", views.compare),
    path("ajax/validate_spotify_usernames", views.validate_spotify_usernames),
    path("ajax/validate_usernames", views.validate_usernames),
    path("ajax/check_access_token", views.check_access_token),
    path("ajax/update", views.update),
    path("ajax/check_update", views.check_update),
    path("ajax/cache_results", views.cache_results),
    path("", views.home_view, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("verify/", views.verify, name="verify"),
    path("callback/", views.callback, name="callback"),
    path("account/", views.account_view, name="account"),
    path("forgot_password/", views.forgot_password_view, name="forgot_password"),
    path("account/reset_password", views.reset_password, name="reset_password"),
    path("account/<str:encr_message>/", views.account_message, name="account_message"),
    path("ajax/validate_username", views.validate_username, name="validate_username"),
    path("ajax/set_email", views.set_email),

]