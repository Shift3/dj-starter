from .base import *
from .base import env

# Site
# https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS += ("gunicorn",)
CORS_ALLOWED_ORIGINS = [CLIENT_URL]

# Storage locaton for uploaded files and static files is S3.
# http://django-storages.readthedocs.org/en/latest/index.html
INSTALLED_APPS += ("storages",)
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
AWS_STORAGE_BUCKET_NAME = env.str("S3_BUCKET")
AWS_DEFAULT_ACL = "public-read"
AWS_AUTO_CREATE_BUCKET = False
AWS_QUERYSTRING_AUTH = False
MEDIA_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/"

# Use AWS SES for sending emails.
EMAIL_BACKEND = "django_ses.SESBackend"
AWS_SES_REGION_NAME = "us-west-2"
AWS_SES_REGION_ENDPOINT = "email.us-west-2.amazonaws.com"

# https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching#cache-control
# Response can be cached by browser and any intermediary caches (i.e. it is "public") for up to 1 day
# 86400 = (60 seconds x 60 minutes x 24 hours)
AWS_HEADERS = {
    "Cache-Control": "max-age=86400, s-maxage=86400, must-revalidate",
}

# Disable browsable api in production
if REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] is not None:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = list(
        REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"]
    )
    if (
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer"
        in REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"]
    ):
        REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].remove(
            "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer"
        )
    if (
        "rest_framework.renderers.BrowsableAPIRenderer"
        in REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"]
    ):
        REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].remove(
            "rest_framework.renderers.BrowsableAPIRenderer"
        )
