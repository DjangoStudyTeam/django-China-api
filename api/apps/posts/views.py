from django.shortcuts import render  # noqa F405
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Post
from .permissions import IsOwner
from .serializers import PostCreateSerializer, PostListSerializer


class PostViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.filter(deleted=False).order_by("-created_at")
        return queryset

    def get_permissions(self):
        if self.action in {"retrieve", "list"}:
            return [AllowAny()]
        elif self.action in {"create", "partial_update"}:
            return [IsAuthenticated(), IsOwner()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in {"retrieve", "list"}:
            return PostListSerializer
        elif self.action in {"create", "partial_update"}:
            return PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
