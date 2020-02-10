from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("verify/", views.verify, name="verify"),
    path("callback/", views.callback, name="callback"),
    path("ajax/validate_username", views.validate_username, name="validate_username")

]