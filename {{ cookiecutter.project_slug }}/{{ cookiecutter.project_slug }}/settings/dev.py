from .base import *
from .base import env

DEBUG = True

INSTALLED_APPS += ("debug_toolbar", "mail_panel")

DEBUG_TOOLBAR_PANELS = [
    "mail_panel.panels.MailToolbarPanel",
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
EMAIL_HOST = "localhost"
EMAIL_PORT = 1025
EMAIL_BACKEND = "mail_panel.backend.MailToolbarBackend"

# CORS
CORS_ALLOW_ALL_ORIGINS = True
