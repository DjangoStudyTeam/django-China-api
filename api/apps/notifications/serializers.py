from notifications_plus.serializers import NotificationListSerializer


class NotificationCreateSerializer(NotificationListSerializer):
    class Meta(NotificationListSerializer.Meta):
        fields = NotificationListSerializer.Meta.fields
