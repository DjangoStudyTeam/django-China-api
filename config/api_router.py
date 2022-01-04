import posts.views
import users.views
from django.urls import path
from rest_framework_extensions.routers import ExtendedDefaultRouter

router = ExtendedDefaultRouter()

router.register("auth", users.views.AuthViewSet, basename="auth")

app_name = "api"
urlpatterns = router.urls + [
    path("posts/", posts.views.PostViewSet.as_view({"post": "post"}), name="posts"),
    path("posts/<pk>/", posts.views.PostViewSet.as_view({"get": "get_retrieve", "patch": "patch"}), name="posts"),
]
