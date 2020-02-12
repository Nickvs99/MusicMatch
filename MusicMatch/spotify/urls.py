from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.stats, name="stats"),
    path("compare/<str:username1>/<str:username2>/", views.compare, name="compare"),
    path("compare/", views.compare_redirect, name="compare_redirect"),
    path("playlist/<str:username1>/<str:username2>/", views.playlist, name="playlist"),
    path("ajax/stats", views.get_stats)
]