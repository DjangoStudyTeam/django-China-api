from django.contrib import admin

from .models import Invitation


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "code",
        "expire_at",
        "expired",
        "valid",
        "invalidated_at",
        "special",
        "creator",
        "invitee",
    ]
    filter_horizontal = ["titles"]
    list_select_related = [
        "creator",
        "invitee",
    ]
    exclude = [
        "code",
        "valid",
        "invalidated_at",
        "creator",
        "invitee",
    ]

    def save_model(self, request, obj, form, change):
        if obj.creator is None:
            obj.creator = request.user
        super().save_model(request, obj, form, change)
