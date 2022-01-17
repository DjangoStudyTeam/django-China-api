import comments.views
import posts.views
import users.views
from rest_framework_extensions.routers import ExtendedDefaultRouter

router = ExtendedDefaultRouter()

router.register("auth", users.views.AuthViewSet, basename="auth")
posts_router = router.register("posts", posts.views.PostViewSet, basename="posts")
router.register("comments", comments.views.CommentCreateUpdateViewSet, basename="comment")
posts_router.register(
    "comments",
    comments.views.CommentListNestedViewSet,
    basename="posts-comment",
    parents_query_lookups=["post_id"],
)

app_name = "api"
urlpatterns = router.urls + []
