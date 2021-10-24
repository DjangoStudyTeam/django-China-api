from djoser.email import ActivationEmail
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import signals
from .serializers import RegisterSerializer, UserSerializer


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = None
    # disable csrf check in SessionAuthentication
    authentication_classes = [TokenAuthentication]

    def get_serializer_class(self):
        if self.action == "register":
            return RegisterSerializer
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
