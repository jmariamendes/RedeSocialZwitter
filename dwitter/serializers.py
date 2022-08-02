from abc import ABC

from rest_framework import serializers
from django.contrib.auth.models import User
# from .models import Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'last_login', 'email', 'date_joined')


'''class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['user', 'follows', 'followed_by']'''


class SeguindoSerializer(serializers.Serializer):
    seguindo = serializers.ListField(child=serializers.CharField(max_length=150))


class SeguidoresSerializer(serializers.Serializer):
    seguidores = serializers.ListField(child=serializers.CharField(max_length=150))


class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    seguindo = SeguindoSerializer(many=True)
    seguidores = SeguidoresSerializer(many=True)


'''class UserProfileSerializer(serializers.ModelSerializer):
    profiles=ProfileSerializer(many=True)

    class Meta:
        model = User
        fields = ['username', 'profiles']'''

