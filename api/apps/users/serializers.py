from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.ImageField(source="avatar_thumbnail")

    class Meta:
        model = User
        fields = ["id", "username", "nickname", "avatar_url"]


class RegisterSerializer(UserCreatePasswordRetypeSerializer):
    email = serializers.EmailField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]

        user = User.objects.filter(username=username).first()

        if not user or not user.check_password(password):
            msg = _("Unable to login with provided credentials.")
            raise serializers.ValidationError(msg)
        if user.is_active == 0:
            msg = _("User account is disabled")
            raise serializers.ValidationError(msg)
        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Token
        fields = ["key", "user"]
