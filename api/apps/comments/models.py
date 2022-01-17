from django.db import models
from posts.models import Post
from tree_comments.models import AbstractTreeComment


class Comment(AbstractTreeComment):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
