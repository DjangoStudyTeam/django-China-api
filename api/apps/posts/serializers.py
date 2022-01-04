from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Post


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "body",
            "views",
            "created_at",
            "user",
            "node",
            "pinned",
            "highlighted",
            "edited_at",
        ]
        extra_kwargs = {
            "pinned": {"required": False},
            "highlighted": {"required": False},
            "user": {"write_only": True},
            "node": {"write_only": True},
        }
        read_only_fields = ["created_at", "edited_at"]

    def validate_views(self, value):
        if value < 0:
            raise ValidationError("请输入大于0的数")
        return value


class PostsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "body",
            "views",
            "pinned",
            "highlighted",
        ]

    def validate_views(self, value):
        if value < 0:
            raise ValidationError("请输入大于0的数")
        return value
