from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("verify/", views.verify, name="verify"),
    path("callback/", views.callback, name="callback"),
    path("account/<str:message>/", views.account_message),
    path("ajax/validate_username", views.validate_username, name="validate_username")

]