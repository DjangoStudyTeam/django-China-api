from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from djoser.serializers import UserCreatePasswordRetypeSerializer, SetPasswordRetypeSerializer
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

        user = authenticate(
            request=self.context.get("request"),
            username=username, password=password
        )
        if not user:
            msg = _("Unable to login with provided credentials.")
            raise serializers.ValidationError(msg)
        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Token
        fields = ["key", "user"]


class PasswordSerializer(SetPasswordRetypeSerializer):
    def validate_current_password(self, value):
        is_password_valid = self.context["request"].user.check_password(value)
        if is_password_valid:
            return value
        else:
            raise serializers.ValidationError("Invalid password.")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs["new_password"] == attrs["re_new_password"]:
            return attrs
        else:
            raise serializers.ValidationError("The two password fields didn't match.")
