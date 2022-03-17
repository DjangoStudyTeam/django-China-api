from notifications_plus.viewsets import NotificationViewSet
from rest_framework import mixins

from .serializers import NotificationCreateSerializer


class NotificationCreateViewSet(mixins.CreateModelMixin, NotificationViewSet):
    serializer_class = NotificationCreateSerializer
