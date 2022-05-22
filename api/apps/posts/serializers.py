from nodes.serializers import NodeListSerializer
from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "body",
            "node",
            "views",
            "pinned",
            "highlighted",
            "deleted",
            "created_at",
            "edited_at",
            "modified_at",
            "user",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "edited_at",
            "modified_at",
            "pinned",
            "highlighted",
            "deleted",
            "views",
        ]


class PostListSerializer(serializers.ModelSerializer):
    node = NodeListSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "body",
            "views",
            "user",
            "pinned",
            "highlighted",
            "deleted",
            "created_at",
            "edited_at",
            "modified_at",
            "node",
        ]
