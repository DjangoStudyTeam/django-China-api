from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ImageField(source="avatar_thumbnail")

    class Meta:
        model = User
        fields = ["id", "username", "nickname", "avatar_url"]


class RegisterSerializer(UserCreatePasswordRetypeSerializer):
    email = serializers.EmailField()
