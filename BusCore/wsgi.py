import os
from django.core.wsgi import get_wsgi_application
import environ

env = environ.Env()
environ.Env.read_env()  

os.environ['DJANGO_SETTINGS_MODULE'] = env('DJANGO_SETTINGS_MODULE')

application = get_wsgi_application()