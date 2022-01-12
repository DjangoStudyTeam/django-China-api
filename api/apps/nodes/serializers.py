from rest_framework import serializers

from .models import Node


class NodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ["id", "created_at", "modified_at", "name", "slug", "cover", "description", "parent"]
