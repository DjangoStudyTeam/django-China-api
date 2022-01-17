from tree_comments.serializers import TreeCommentCreateSerializer


class CommentCreateSerializer(TreeCommentCreateSerializer):
    class Meta(TreeCommentCreateSerializer.Meta):
        fields = TreeCommentCreateSerializer.Meta.fields + ["post"]
