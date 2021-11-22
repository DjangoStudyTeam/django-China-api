from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.contrib.auth.tokens import default_token_generator
from djoser.conf import settings
from djoser.email import ActivationEmail, PasswordResetEmail, ConfirmationEmail
from djoser.serializers import SendEmailResetSerializer, PasswordResetConfirmSerializer, ActivationSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from . import signals
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, TokenSerializer, PasswordSerializer

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = None
    # disable csrf check in SessionAuthentication
    authentication_classes = [TokenAuthentication]
    token_generator = default_token_generator

    def get_serializer_class(self):
        if self.action == "register":
            return RegisterSerializer
        elif self.action == "login":
            return LoginSerializer
        elif self.action == "change_password":
            return PasswordSerializer
        elif self.action == "forgot_password":
            return SendEmailResetSerializer
        elif self.action == "reset_password":
            return PasswordResetConfirmSerializer
        elif self.action == "activate":
            return ActivationSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="Register",
        responses={201: UserSerializer},
    )
    @action(
        ["POST"],
        detail=False,
        url_path="register",
        url_name="register",
        serializer_class=RegisterSerializer,
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )
        context = {"user": user}
        to = [user.email]
        ActivationEmail(self.request, context).send(to)
        output_serializer = UserSerializer(
            instance=user, context={"request": request})
        return Response(
            data=output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Login",
        request=LoginSerializer,
        responses={200: TokenSerializer},
    )
    @action(
        ["POST"],
        detail=False,
        url_name="login",
        url_path="login",
        serializer_class=TokenSerializer,
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        Token.objects.filter(user=user).delete()
        token, _ = Token.objects.get_or_create(user=user)
        user_logged_in.send(
            sender=self.__class__, user=user, request=self.request
        )
        output_serializer = TokenSerializer(
            token, context={"request": request})
        return Response(
            data=output_serializer.data,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        summary="Logout",
    )
    @action(
        ["POST"],
        detail=False,
        url_name="logout",
        url_path="logout",
        permission_classes=[IsAuthenticated]
    )
    def logout(self, request):
        Token.objects.filter(user=request.user).delete()
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        summary="change_password",
        request=PasswordSerializer,
    )
    @action(
        ["POST"],
        detail=False,
        url_name="change_password",
        url_path="change_password",
        permission_classes=[IsAuthenticated]
    )
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_password()
        signals.user_password_changed.send(
            sender=request.user.__class__, request=request, user=request.user
        )
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        summary="forgot_password",
        request=SendEmailResetSerializer,
        responses=None
    )
    @action(
        ["POST"],
        detail=False,
        url_name="forgot_password",
        url_path="forgot_password",
    )
    def forgot_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()
        if user:
            context = {"user": user}
            to = [user.email]
            PasswordResetEmail(self.request, context).send(to)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"email_not_found": "User with given email does not exist."}
            )

    @extend_schema(
        summary="reset_password",
        responses=None
    )
    @action(
        ["POST"],
        detail=False,
        url_path="reset_password",
        url_name="reset_password",
    )
    def reset_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.set_password(serializer.data["new_password"])
        return Response(status=status.HTTP_200_OK)

    @extend_schema(
        summary="Activate",
        responses=None
    )
    @action(
        ["POST"],
        detail=False,
        url_name="activate",
        url_path="activate"
    )
    def activate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [user.email]
            ConfirmationEmail(self.request, context).send(to)

        return Response(status=status.HTTP_200_OK)
