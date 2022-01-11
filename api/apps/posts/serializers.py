from nodes.serializers import NodeListSerializer
from rest_framework import serializers

from .models import Post


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "body",
            "node",
            "views",
            "user",
            "pinned",
            "highlighted",
            "deleted",
            "created_at",
            "edited_at",
            "modified_at",
        ]
        read_only_fields = [
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

    class Meta:
        model = Post
        fields = [
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
