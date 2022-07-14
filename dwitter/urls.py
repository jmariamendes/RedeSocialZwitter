# dwitter/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


app_name = "dwitter"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("password_change_done/", views.password_change_done, name="password_change_doner"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile_list/", views.profile_list, name="profile_list"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path("accounts/password_change_done/", views.password_change_done, name="password_change_doner"),
    path("convites/", views.convites, name="convites"),
    path("trata_convite/<int:pk>", views.trata_convite, name="trata_convite"),
    path("mensagens/", views.mensagens, name="mensagens"),
    path("trata_msg_user/<int:pk>", views.trata_msg_user, name="trata_msg_user"),
    path("convidar_amigo", views.convidar_amigo, name="convidar_amigo"),
    path("convite_enviado", views.convite_enviado, name="convite_enviado"),
]
