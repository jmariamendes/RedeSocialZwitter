# dwitter/urls.py

from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import dashboard, profile_list, profile, register

app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>", profile, name="profile"),
    path("register/", register, name="register"),
]
