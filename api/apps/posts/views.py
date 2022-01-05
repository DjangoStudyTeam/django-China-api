from django.shortcuts import render  # noqa F405
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Post
from .serializers import PostCreateSerializer, PostListSerializer


class PostViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    serializer_class = None
    queryset = Post.objects.filter(deleted=False)

    def get_permissions(self):
        if self.action == "retrieve":
            self.permission_classes = [AllowAny]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "update":
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostListSerializer
        elif self.action == "create":
            return PostCreateSerializer
        elif self.action == "update":
            return PostCreateSerializer
