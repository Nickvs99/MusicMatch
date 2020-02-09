from django.urls import path
from . import views

urlpatterns = [
    path("stats/<str:username>/", views.stats, name="stats"),
    path("stats/", views.stats_redirect, name="stats_redirect"),
    path("compare/<str:username1>/<str:username2>/", views.compare, name="compare"),
    path("compare/", views.compare_redirect, name="compare_redirect"),
    path("playlist/<str:username1>/<str:username2>/", views.playlist, name="playlist"),

]