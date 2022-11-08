from .base import *
from .base import env

DEBUG = True

INSTALLED_APPS += ("debug_toolbar", )

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
]

MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

# Mail
# Visit http://localhost:8025/ to see outgoing mail. A mailhog instance
# is served from that address in development.
EMAIL_HOST = env.str("EMAIL_HOST", "mailhog")
EMAIL_PORT = 1025
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# CORS
CORS_ALLOW_ALL_ORIGINS = True
