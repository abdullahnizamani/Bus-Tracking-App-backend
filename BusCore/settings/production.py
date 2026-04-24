from .base import *
import dj_database_url
DEBUG = True

DATABASES = {
    'default': dj_database_url.config(
    conn_max_age=600,
    conn_health_checks=True,
)
}

ALLOWED_HOSTS = ['*']
MIDDLEWARE+=['whitenoise.middleware.WhiteNoiseMiddleware']
STATIC_ROOT = BASE_DIR / 'staticfiles'