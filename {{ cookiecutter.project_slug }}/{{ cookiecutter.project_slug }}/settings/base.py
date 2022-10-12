import os
import socket
import dj_database_url
import redis
import environ
from os.path import join

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# If you have a .env file it will be imported here. Currently one is
# not needed for local development but can be used if you want to run
# outside of the dev docker container, or customize it for your local
# environment in some way.
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

# Set DEBUG to False as a default for safety
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
ALLOWED_HOSTS = ["*"]
DEBUG = env.bool("DJANGO_DEBUG", False)

SERVER_URL = env.str("SERVER_URL", "http://localhost:8000")
CLIENT_URL = env.str("CLIENT_URL", "http://localhost:4200")
DEFAULT_FROM_EMAIL = f'no-reply@{env.str("EMAIL_DOMAIN", "localhost")}'
SERVER_EMAIL = f'root@{env.str("EMAIL_DOMAIN", "localhost")}'
SEEDED_USER_EMAIL = env.str("SEEDED_USER_EMAIL", None)

INSTALLED_APPS = (
    # Builtin apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Health check
    "health_check",
    "health_check.db",
    "health_check.contrib.migrations",

    # Third party apps
    "channels",
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "django_filters",
    "django_extensions",
    "simple_history",
    "phonenumber_field",
    "easy_thumbnails",
    "django_dramatiq",
    "djstripe",

    # Your apps
    "{{ cookiecutter.project_slug }}.core",
    "{{ cookiecutter.project_slug }}.users",
    "{{ cookiecutter.project_slug }}.agents",
{%- if cookiecutter.include_notifications == "yes" %}
    "django_eventstream",
    "{{ cookiecutter.project_slug }}.notification_system",
{%- endif %}
    "{{ cookiecutter.project_slug }}.payments",
)

# https://docs.djangoproject.com/en/4.0/topics/http/middleware/
MIDDLEWARE = (
    "corsheaders.middleware.CorsMiddleware",
{%- if cookiecutter.include_notifications == "yes" %}
    "django_grip.GripMiddleware",
{%- endif %}
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
)

hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"
SECRET_KEY = env.str("DJANGO_SECRET_KEY")
WSGI_APPLICATION = "{{ cookiecutter.project_slug }}.wsgi.application"

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

ADMINS = (("Author", "jschiff@bitwiseindustries.com"),)

# Postgres
DATABASES = {
    "default": dj_database_url.config(
        default="postgres://postgres:@postgres:5432/{{ cookiecutter.project_slug }}",
        conn_max_age=env.int("POSTGRES_CONN_MAX_AGE", 600),
    )
}

# General
APPEND_SLASH = False
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)
USE_TZ = True
LOGIN_REDIRECT_URL = "/"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
STATIC_ROOT = os.path.normpath(join(os.path.dirname(BASE_DIR), "static"))
STATICFILES_DIRS = []
STATIC_URL = "/static/"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Media files
MEDIA_ROOT = join(os.path.dirname(BASE_DIR), "media")
MEDIA_URL = "/media/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR), "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Password Validation
# https://docs.djangoproject.com/en/4.0/topics/auth/passwords/#module-django.contrib.auth.password_validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[%(server_time)s] %(message)s",
        },
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
        },
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {"handlers": ["console"], "level": "INFO"},
    },
}

# Custom user app
AUTH_USER_MODEL = "users.User"

# Phone number setup
PHONENUMBER_DEFAULT_REGION = "US"

# Shell Plus (django-extensions)
# https://django-extensions.readthedocs.io/en/latest/shell_plus.html#
SHELL_PLUS_PRINT_SQL_TRUNCATE = None

# Easy Thumbnailer
THUMBNAIL_ALIASES = {
    # Global Aliases
    "": {
        "xs": {"size": (32, 32), "crop": True},
        "sm": {"size": (64, 64), "crop": True},
        "md": {"size": (128, 128), "crop": True},
    }
}

# Django Rest Framework
PAGINATION_MAX_PAGE_SIZE = 10000
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "{{ cookiecutter.project_slug }}.core.pagination.LinkedPagination",
    "PAGE_SIZE": env.int("DJANGO_PAGINATION_LIMIT", 10),
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
    },
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
}

DJOSER = {
    "HIDE_USERS": False,
    "SEND_ACTIVATION_EMAIL": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "ACTIVATION_URL": "/auth/activate-account/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL": "/auth/reset-password/{uid}/{token}",
    # This is not provided by djoser, but we follow djoser
    # conventions here anyway
    "CHANGE_EMAIL_REQUEST_URL": "/auth/confirm-change-email/{uid}/{token}",
    "PERMISSIONS": {
        "user_delete": ["{{ cookiecutter.project_slug }}.users.permissions.IsAdmin"],
        "user_list": ["{{ cookiecutter.project_slug }}.users.permissions.IsAdmin"],
    },
    "EMAIL": {
        "activation": "{{ cookiecutter.project_slug }}.users.email.ActivationEmail",
        "password_reset": "{{ cookiecutter.project_slug }}.users.email.PasswordResetEmail",
    },
    "SERIALIZERS": {
        "user": "{{ cookiecutter.project_slug }}.users.serializers.UserSerializer",
        "user_delete": "rest_framework.serializers.Serializer",
        "token": "{{ cookiecutter.project_slug }}.users.serializers.TokenSerializer",
        "user_create": "{{ cookiecutter.project_slug }}.users.serializers.UserCreateSerializer",
        "current_user": "{{ cookiecutter.project_slug }}.users.serializers.UserSerializer",
        "create_user": "{{ cookiecutter.project_slug }}.users.serializers.UserCreateSerializer",
        "activation": "{{ cookiecutter.project_slug }}.users.serializers.ActivationSerializer",
    },
}

# Tasks
DRAMATIQ_REDIS_URL = env.str("REDIS_URL", "redis://redis:6379/0")
DRAMATIQ_BROKER = {
    "BROKER": "dramatiq.brokers.redis.RedisBroker",
    "OPTIONS": {
        "connection_pool": redis.ConnectionPool.from_url(DRAMATIQ_REDIS_URL),
    },
    "MIDDLEWARE": [
        "dramatiq.middleware.AgeLimit",
        "dramatiq.middleware.TimeLimit",
        "dramatiq.middleware.Retries",
        "django_dramatiq.middleware.AdminMiddleware",
        "django_dramatiq.middleware.DbConnectionsMiddleware",
    ],
}

# Simple History
SIMPLE_HISTORY_FILEFIELD_TO_CHARFIELD = True

# Django Channels
# https://channels.readthedocs.io/en/stable/topics/channel_layers.html
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
ASGI_APPLICATION = '{{ cookiecutter.project_slug }}.asgi.application'

# Twilio Integration
TWILIO_FROM_NUMBER = env.str("TWILIO_FROM_NUMBER", None)
TWILIO_ACCOUNT_SID = env.str("TWILIO_ACCOUNT_SID", None)
TWILIO_AUTH_TOKEN = env.str("TWILIO_AUTH_TOKEN", None)

{%- if cookiecutter.include_notifications == "yes" %}
# Django Eventstream
# https://github.com/fanout/django-eventstream
# 
# Enables the easy use of SSE (Server sent events) we use this for
# notifications.
# EVENTSTREAM_CHANNELMANAGER_CLASS = '{{ cookiecutter.project_slug }}.core.channelmanager.UserChannelManager'
EVENTSTREAM_ALLOW_ORIGIN = CLIENT_URL
EVENTSTREAM_ALLOW_CREDENTIALS = True
NOTIFICATION_TOKEN_EXPIRATION_SECONDS = 30
{%- endif %}

# When using the `image_size_validator`, this sets the maximum size
# that will be accepted. Make sure that in production, your
# nginx/apache is configure to accept body content up to or above the
# size you set here.
MAX_IMAGE_UPLOAD_SIZE_MB = 20

STRIPE_LIVE_MODE = False
STRIPE_SECRET_KEY= env.str("STRIPE_SECRET_KEY", None)
STRIPE_TEST_SECRET_KEY= env.str("STRIPE_SECRET_KEY", None)
STRIPE_LIVE_SECRET_KEY= env.str("STRIPE_SECRET_KEY", None)
DJSTRIPE_WEBHOOK_SECRET = env.str("DJSTRIPE_WEBHOOK_SECRET", "")
DJSTRIPE_WEBHOOK_VALIDATION = None
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "djstripe_id"
