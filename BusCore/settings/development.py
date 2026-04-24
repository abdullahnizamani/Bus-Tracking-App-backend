from base import *
DEBUG = True
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
