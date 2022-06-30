from .common import *  # noqa
from .common import env

SECRET_KEY = env.str("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
CORS_ORIGIN_ALLOW_ALL = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db("DJANGO_DATABASE_DEFAULT_URL")}  # noqa F405
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # noqa F405
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405

# EMAIL
# -----------------------------------------------------------------
EMAIL_HOST = env.str("DJANGO_EMAIL_HOST")
EMAIL_HOST_USER = env.str("DJANGO_EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("DJANGO_EMAIL_HOST_PASSWORD")
EMAIL_PORT = env.int("DJANGO_EMAIL_PORT")
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
