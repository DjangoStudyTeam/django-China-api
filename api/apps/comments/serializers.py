from tree_comments.serializers import TreeCommentCreateSerializer

from .models import Comment


class CommentCreateSerializer(TreeCommentCreateSerializer):
    class Meta(TreeCommentCreateSerializer.Meta):
        model = Comment
        fields = TreeCommentCreateSerializer.Meta.fields + ["post"]
