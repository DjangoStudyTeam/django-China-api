from django.contrib.contenttypes.models import ContentType
from tree_comments.viewsets import TreeCommentCreateUpdateViewSet, TreeCommentListViewSet

from . import signals
from .models import Comment
from .serializers import CommentCreateSerializer


class CommentCreateUpdateViewSet(TreeCommentCreateUpdateViewSet):
    create_serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        content_type = ContentType.objects.get(model=Comment._meta.model_name)
        signals.comment_posted.send(sender=Comment, instance=serializer.instance, content_type=content_type)


class CommentListNestedViewSet(TreeCommentListViewSet):
    ...
