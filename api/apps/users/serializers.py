from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
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
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username, password=password
            )
            if not user:
                user = User.objects.filter(username=username).first()
                if user and not user.check_password(password):
                    msg = _("用户名或密码错误")
                    raise serializers.ValidationError(msg)
            if user and not user.is_active:
                msg = _("用户未激活")
                raise serializers.ValidationError(msg)
            if user and user.is_active:
                attrs['user'] = user
                return attrs
        else:
            msg = _("必须包含 username 和 password 字段")
            raise serializers.ValidationError(msg)