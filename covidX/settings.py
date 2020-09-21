"""
Django settings for covidX project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import os
import sys

from covidX import gae_settings as gae


PROJECT_NAME = "covidX"
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 1800,
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
# When running on GAE, access from gcp secret manager.
SECRET_KEY = os.getenv("SECRET_KEY", gae.access_secret_key_version())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG_ENV", None))

ALLOWED_HOSTS = [
    "*",
    os.getenv("DJANGO_ALLOWED_HOST", "127.0.0.1"),
    "localhost",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "social_django",
    "django_extensions",
    "graphene_django",
    "corsheaders",
    "apps.hrm.apps.HrmConfig",
    "apps.apihealth.apps.APIHealthConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "covidX.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "apps/auth/templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

WSGI_APPLICATION = "covidX.wsgi.application"

ASGI_APPLICATION = "covidX.asgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

if os.getenv("GAE_APPLICATION", None):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "HOST": f'/cloudsql/{os.getenv("CONNECTION_NAME")}',
            "USER": f'{os.getenv("DB_USER")}',
            "PASSWORD": f'{os.getenv("DB_PWD")}',
            "NAME": f'{os.getenv("DB_NAME")}',
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "HOST": "localhost",
            "PORT": os.getenv("DB_PORT", "5432"),
            "NAME": "covid",
            "USER": "covid",
            "PASSWORD": "postgres",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # pylint: disable=line-too-long
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(os.path.join(PROJECT_ROOT, "apps/"))

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"


# SOCIAL AUTH AUTH0 BACKEND CONFIG
SOCIAL_AUTH_TRAILING_SLASH = False
SOCIAL_AUTH_AUTH0_KEY = os.environ.get("AUTH0_CLIENT_ID")
SOCIAL_AUTH_AUTH0_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
SOCIAL_AUTH_AUTH0_SCOPE = ["openid", "profile", "email"]
SOCIAL_AUTH_AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUDIENCE = None
if os.environ.get("AUTH0_AUDIENCE"):
    AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
else:
    if SOCIAL_AUTH_AUTH0_DOMAIN:
        AUDIENCE = f"https://{SOCIAL_AUTH_AUTH0_DOMAIN}/userinfo"
if AUDIENCE:
    SOCIAL_AUTH_AUTH0_AUTH_EXTRA_ARGUMENTS = {"audience": AUDIENCE}
AUTHENTICATION_BACKENDS = {
    "apps.auth.auth0backend.Auth0",
    "django.contrib.auth.backends.ModelBackend",
}

LOGIN_URL = "/login/auth0"
LOGIN_REDIRECT_URL = "/dashboard"
GRAPHENE = {
    "SCHEMA": "covidX.schema.schema",
    "SCHEMA_OUTPUT": "schema.json",
    "SCHEMA_INDENT": 2,
}
