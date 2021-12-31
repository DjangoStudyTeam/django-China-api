from rest_framework import serializers

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "title",
            "body",
            "views",
            "created_at",
            "modified_at",
            "user",
            "node",
            "deleted",
            "pinned",
            "highlighted",
            "edited_at",
        ]
        extra_kwargs = {
            "deleted": {"write_only": True, "required": False},
            "pinned": {"required": False},
            "highlighted": {"required": False},
            "user": {"write_only": True},
            "node": {"write_only": True},
        }
        read_only_fields = ["created_at", "modified_at", "edited_at"]
