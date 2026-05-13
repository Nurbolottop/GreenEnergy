from core.settings.base import *

DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ["greenenergy.su", "www.greenenergy.su"]

CSRF_TRUSTED_ORIGINS = [
    "https://greenenergy.su",
    "https://www.greenenergy.su",
]

STATIC_ROOT = "/app/staticfiles"
