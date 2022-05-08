from actstream.actions import follow, unfollow
from django.shortcuts import render  # noqa F405
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

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

    @action(methods=["POST"], detail=True, url_path="favourites", url_name="favourite")
    def create_favourite(self, request, *args, **kwargs):
        post = self.get_object()
        follow(request.user, post, send_action=True, flag="favourite")
        return Response(status=status.HTTP_201_CREATED)

    @create_favourite.mapping.delete
    def destroy_favourite(self, request, *args, **kwargs):
        post = self.get_object()
        unfollow(request.user, post, flag="favourite")
        return Response(status=status.HTTP_204_NO_CONTENT)
