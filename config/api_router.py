import posts.views
import users.views
from rest_framework_extensions.routers import ExtendedDefaultRouter

router = ExtendedDefaultRouter()

router.register("auth", users.views.AuthViewSet, basename="auth")
router.register("posts", posts.views.PostViewSet, basename="posts")

app_name = "api"
urlpatterns = router.urls + []
