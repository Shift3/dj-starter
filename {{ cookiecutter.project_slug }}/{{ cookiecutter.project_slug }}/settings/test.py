from .base import *
from .base import env


SECRET_KEY = "test"

# Use a faster password hasher during testing.
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
