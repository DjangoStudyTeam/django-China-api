from tree_comments.viewsets import (
    TreeCommentCreateUpdateViewSet,
    TreeCommentListViewSet,
)

from .serializers import CommentCreateSerializer


class CommentCreateUpdateViewSet(TreeCommentCreateUpdateViewSet):
    create_serializer_class = CommentCreateSerializer


class CommentListNestedViewSet(TreeCommentListViewSet):
    ...
