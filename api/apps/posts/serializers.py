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
            "edited_at",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "created_at",
            "edited_at",
            "modified_at",
            "pinned",
            "highlighted",
            "deleted",
            "user",
            "views",
        ]


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
