from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.stats, name="stats"),
    path("compare/", views.compare, name="compare"),
    path("playlist/<str:username1>/<str:username2>/", views.playlist, name="playlist"),
    path("ajax/stats", views.get_stats),
    path("ajax/compare", views.get_comparison),
]