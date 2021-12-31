import posts.views
import users.views
from django.urls import path
from rest_framework_extensions.routers import ExtendedDefaultRouter

router = ExtendedDefaultRouter()

router.register("auth", users.views.AuthViewSet, basename="auth")
# router.register("posts", posts.views.PostViewSet, basename="posts")
app_name = "api"
urlpatterns = router.urls + [
    path("posts/", posts.views.PostViewSet.as_view({"post": "post_create"})),
    path("posts/<pk>/", posts.views.PostViewSet.as_view({"get": "get_retrieve"})),
]
