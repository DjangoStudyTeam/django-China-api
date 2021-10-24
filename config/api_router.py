import users.views
from rest_framework_extensions.routers import ExtendedSimpleRouter

router = ExtendedSimpleRouter()

router.register("auth", users.views.AuthViewSet, basename="auth")

app_name = "api"
urlpatterns = router.urls + []
