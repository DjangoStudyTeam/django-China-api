from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from djoser.email import ActivationEmail
from djoser.serializers import TokenSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import signals
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer


User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = None
    # disable csrf check in SessionAuthentication
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action == "register":
            return RegisterSerializer
        elif self.action == "login":
            return LoginSerializer
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
        output_serializer = UserSerializer(instance=user, context={"request": request})
        return Response(
            data=output_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Login",
        responses={200: LoginSerializer},
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
        output_serializer = TokenSerializer(token, context={"request": request})
        return Response(
            data=output_serializer.data,
            status=status.HTTP_200_OK
        )
