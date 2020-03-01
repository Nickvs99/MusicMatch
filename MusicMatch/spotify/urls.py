from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.stats, name="stats"),
    path("compare/", views.compare, name="compare"),
    path("update/", views.update_view, name="update"),
    path("ajax/playlist", views.playlist, name="playlist"),
    path("ajax/stats", views.get_stats),
    path("ajax/compare", views.get_comparison),
    path("ajax/validate_spotify_usernames", views.validate_spotify_usernames),
    path("ajax/validate_usernames", views.validate_usernames),
    path("ajax/write_data", views.write_data),
    path("ajax/check_access_token", views.check_access_token),
    path("ajax/update", views.update),
    path("ajax/check_update", views.check_update),
]