from actstream.actions import follow
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from tree_comments.viewsets import (
    TreeCommentCreateUpdateViewSet,
    TreeCommentListViewSet,
)

from .serializers import CommentCreateSerializer


class CommentCreateUpdateViewSet(TreeCommentCreateUpdateViewSet):
    create_serializer_class = CommentCreateSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="likes",
        url_name="like",
        permission_classes=[permissions.IsAuthenticated],
    )
    def create_like(self, request, *args, **kwargs):
        comment = self.get_object()
        follow(request.user, comment, send_action=True, flag="like")
        return Response(status=status.HTTP_201_CREATED)


class CommentListNestedViewSet(TreeCommentListViewSet):
    ...
