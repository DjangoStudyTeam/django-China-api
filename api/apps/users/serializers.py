from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from djoser.conf import settings
from djoser.serializers import SetPasswordRetypeSerializer, UserCreatePasswordRetypeSerializer
from invitations.models import Invitation
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
    invitation_code = serializers.CharField()

    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        fields = UserCreatePasswordRetypeSerializer.Meta.fields + ("invitation_code",)

    def perform_create(self, validated_data):
        invitation = validated_data.pop("invitation")
        rows = Invitation.objects.filter(code=invitation.code, valid=True).update(
            valid=False,
            invalidated_at=timezone.now(),
        )
        if rows < 1:
            raise serializers.ValidationError({"invitation_code": _("Invitation code is invalid.")})

        user = User.objects.create_user(
            special=invitation.special,
            inviter=invitation.creator,
            **validated_data,
        )
        invitation.invitee = user
        invitation.save(update_fields=["invitee"])

        for title in invitation.titles.all():
            user.titles.add(title)

        if settings.SEND_ACTIVATION_EMAIL:
            user.is_active = False
            user.save(update_fields=["is_active"])

        return user

    def validate(self, attrs):
        code = attrs.pop("invitation_code")
        validated_data = super().validate(attrs)
        try:
            invitation = Invitation.objects.get(code=code)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError({"invitation_code": _("Invitation code is invalid.")})
        else:
            if not invitation.valid or invitation.expired():
                raise serializers.ValidationError({"invitation_code": _("Invitation code is invalid.")})
            validated_data["invitation"] = invitation

        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("Username"),
    )
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False, write_only=True
    )

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]

        user = authenticate(request=self.context.get("request"), username=username, password=password)
        if not user:
            msg = _("Unable to login with provided credentials.")
            raise serializers.ValidationError(msg)
        attrs["user"] = user
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Token
        fields = ["key", "user"]


class PasswordSerializer(SetPasswordRetypeSerializer):
    def set_password(self):
        new_password = self.validated_data["new_password"]
        user = self.context["request"].user
        user.set_password(new_password)
        user.save()
