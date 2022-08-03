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
        # API´s disponíveis no sistema, via Django/REST
    path("api/v2/usuarios", views.get_usuarios, name="get_usuarios"), # pesquisa todos usuarios
    path("api/v1/usuarios/<str:user>", views.get_update_usuarios, name="get_update_usuarios"), # pesq. usuer por nomw
    path("api/v1/usuario/<int:pk>", views.get_usuario, name="get_usuario"), # pesq. user por Id
    path("api/v1/seguidores/<str:user>", views.get_follows, name="get_follows"), # pesq. seguidores/seguindo do user
]

