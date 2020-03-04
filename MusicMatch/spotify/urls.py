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
]