# !/usr/bin/python3
# -*- coding: utf-8 -*-


from .common import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#*n4l14-4397kxi)(wy7+f1h196$+h_ue1ts&4ui9i$pqn&$fm'

# django-extensions
INSTALLED_APPS += ["django_extensions"]  # noqa F405

ALLOWED_HOSTS = ["*"]
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}