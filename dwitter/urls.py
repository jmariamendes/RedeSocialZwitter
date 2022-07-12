# dwitter/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import dashboard, profile_list, profile, register, convites, trata_convite, password_change_done, mensagens, trata_msg_user


app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("password_change_done/", password_change_done, name="password_change_doner"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("register/", register, name="register"),
    path("accounts/password_change_done/", password_change_done, name="password_change_doner"),
    path("convites/", convites, name="convites"),
    path("trata_convite/<int:pk>", trata_convite, name="trata_convite"),
    path("mensagens/", mensagens, name="mensagens"),
    path("trata_msg_user/<int:pk>", trata_msg_user, name="trata_msg_user"),
]
